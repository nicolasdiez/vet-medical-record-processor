from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import MedicalRecord, Pet
from app.domain.ports.inbound.interfaces import SaveClinicalDataUseCasePort
from app.domain.ports.outbound.interfaces import (
    MedicalRecordRepositoryPort,
    PetRepositoryPort,
)


class SaveClinicalDataUseCase(SaveClinicalDataUseCasePort):
    """
    Application service that orchestrates Phase 3: Validation & Persistence.
    It receives confirmed data from the UI and persists it into the database
    ensuring atomicity (transactional integrity).
    """

    def __init__(
        self,
        pet_repository: PetRepositoryPort,
        medical_record_repository: MedicalRecordRepositoryPort,
        session: AsyncSession  # inject the session to control the transaction (atomic - all or nothing)
    ):
        self.pet_repository = pet_repository
        self.medical_record_repository = medical_record_repository
        self.session = session

    async def execute(self, pet: Pet, records: List[MedicalRecord]) -> None:
        """
        Saves the pet and its medical records in a single transaction.
        If any step fails, the transaction is rolled back.
        """
        try:
            # 1. Persist Pet info (Update or Insert)
            await self.pet_repository.save(pet)

            # 2. Persist all Medical Records associated with this pet
            # ensure consistency by re-assigning the pet_id to every record
            for record in records:
                record.pet_id = pet.id
            
            await self.medical_record_repository.save_bulk(records)

            # 3. Transactional Commit: All or nothing.
            # This is where the actual SQL commands are sent and finalized in the DB file.
            await self.session.commit()

        except Exception as e:
            # If something goes wrong, rollback to keep the database clean
            await self.session.rollback()
            raise RuntimeError(f"Persistence failed: {str(e)}")