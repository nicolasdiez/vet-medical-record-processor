from typing import List, Tuple, Optional

from app.domain.entities import Pet, MedicalRecord
from app.domain.ports.inbound.interfaces import ExtractClinicalDataUseCasePort
from app.domain.ports.outbound.interfaces import (
    FileTextExtractorPort,
    MedicalRecordExtractorPort,
    PetRepositoryPort
)

class ExtractClinicalDataUseCase(ExtractClinicalDataUseCasePort):
    """
    Application service that orchestrates Phase 1: 
    Extracts text from a document, delegates AI processing, and checks for existing entities.
    It does NOT persist data to the database.
    """

    def __init__(
        self,
        medical_extractor: MedicalRecordExtractorPort,
        pet_repository: PetRepositoryPort
    ):
        self.medical_extractor = medical_extractor
        self.pet_repository = pet_repository

    async def execute(self, file_content: bytes, filename: str, file_extractor: FileTextExtractorPort) -> Tuple[Optional[Pet], List[MedicalRecord]]:
        # 1. Extract raw text from the binary document using the injected strategy
        raw_text = await file_extractor.extract_text(file_content, filename)

        # 2. Ask the LLM to extract structured entities from the raw text
        pet, records = await self.medical_extractor.extract_entities(raw_text)

        # 3. Reconcile Pet identity if it already exists in our system
        if pet:
            existing_pet = await self.pet_repository.find_by_name_and_species(pet.name, pet.species)
            
            if existing_pet:
                # The pet exists! Reuse its real ID from the DB so we don't create duplicates later
                pet.id = existing_pet.id
            
            # Ensure all extracted medical records point to the correct Pet ID
            for record in records:
                record.pet_id = pet.id

        return pet, records