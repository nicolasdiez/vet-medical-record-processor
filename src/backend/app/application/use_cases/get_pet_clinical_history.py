from typing import List

from app.domain.entities import MedicalRecord
from app.domain.ports.inbound.interfaces import GetPetClinicalHistoryUseCasePort
from app.domain.ports.outbound.interfaces import MedicalRecordRepositoryPort


class GetPetClinicalHistoryUseCase(GetPetClinicalHistoryUseCasePort):
    """Orchestrates the retrieval of a pet's complete clinical history.

    Attributes:
        medical_record_repository (MedicalRecordRepositoryPort): Outbound port for records.
    """

    def __init__(
        self, 
        medical_record_repository: MedicalRecordRepositoryPort
    ):
        """Initializes the use case with the required repository.

        Args:
            medical_record_repository (MedicalRecordRepositoryPort): Port to fetch records.
        """
        self.medical_record_repository = medical_record_repository

    async def execute(self, pet_id: str) -> List[MedicalRecord]:
        """Retrieves all medical records for the specified pet ID.

        Args:
            pet_id (str): The unique identifier of the pet.

        Returns:
            List[MedicalRecord]: The chronological list of medical records.
        """
        return await self.medical_record_repository.get_by_pet_id(pet_id)