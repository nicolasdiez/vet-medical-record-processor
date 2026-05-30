from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import MedicalRecord, Pet
from app.domain.ports.inbound.interfaces import SaveClinicalDataUseCasePort
from app.domain.ports.outbound.interfaces import (
    MedicalRecordRepositoryPort,
    PetRepositoryPort,
)


class SaveClinicalDataUseCase(SaveClinicalDataUseCasePort):
    """Orchestrates Phase 3 of the Human-in-the-Loop flow: Persistence.

    Receives the validated and potentially user-corrected Domain Entities from the 
    interface and persists them atomically to the database using an active transaction.

    Attributes:
        pet_repository (PetRepositoryPort): Outbound port to save pet data.
        medical_record_repository (MedicalRecordRepositoryPort): Outbound port to save records.
        session (AsyncSession): The database session to manage the transaction.
    """

    def __init__(
        self,
        pet_repository: PetRepositoryPort,
        medical_record_repository: MedicalRecordRepositoryPort,
        session: AsyncSession  # inject the session to control the transaction (atomic:  all or nothing)
    ):
        """Initializes the use case with required repositories and DB session.

        Args:
            pet_repository (PetRepositoryPort): Port for Pet persistence.
            medical_record_repository (MedicalRecordRepositoryPort): Port for MedicalRecord persistence.
            session (AsyncSession): Active SQLAlchemy async session for atomic commits.
        """
        self.pet_repository = pet_repository
        self.medical_record_repository = medical_record_repository
        self.session = session

    async def execute(self, pet: Pet, records: List[MedicalRecord]) -> None:
        """Atomically saves the clinical data into the database.

        Args:
            pet (Pet): The verified Pet domain entity.
            records (List[MedicalRecord]): The verified list of MedicalRecord entities.

        Raises:
            Exception: If the database transaction fails to commit, it will be rolled back.
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