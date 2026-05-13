from typing import List

from app.domain.entities import MedicalRecord
from app.domain.ports.inbound.interfaces import GetPetClinicalHistoryUseCasePort
from app.domain.ports.outbound.interfaces import MedicalRecordRepositoryPort

class GetPetClinicalHistoryUseCase(GetPetClinicalHistoryUseCasePort):
    """
    Application service that retrieves the complete medical history for a given pet.
    """

    def __init__(self, medical_record_repository: MedicalRecordRepositoryPort):
        self.medical_record_repository = medical_record_repository

    async def execute(self, pet_id: str) -> List[MedicalRecord]:
        # Delegate the read operation to the repository adapter
        return await self.medical_record_repository.get_by_pet_id(pet_id)