from typing import List, Optional, Tuple

from app.domain.entities import MedicalRecord, Pet
from app.domain.ports.inbound.interfaces import ExtractClinicalDataUseCasePort
from app.domain.ports.outbound.interfaces import (
    FileTextExtractorPort,
    MedicalRecordExtractorPort,
    PetRepositoryPort,
)


class ExtractClinicalDataUseCase(ExtractClinicalDataUseCasePort):
    """Orchestrates Phase 1 of the Human-in-the-Loop flow: AI Processing.

    Extracts text from a provided clinical document, delegates the processing to an AI 
    model to identify structured entities (Pet and Medical Records), and reconciles the 
    extracted Pet against the database to prevent duplicates. It does NOT persist data.

    Attributes:
        medical_extractor (MedicalRecordExtractorPort): Outbound port to extract medical records from a raw text block.
        pet_repository (PetRepositoryPort): Outbound port to query existing pets.
    """

    def __init__(
        self,
        medical_extractor: MedicalRecordExtractorPort,
        pet_repository: PetRepositoryPort
    ):
        """Initializes the use case with the required repositories.

        Args:
            medical_extractor (MedicalRecordExtractorPort): Port adapter for medical records extraction.
            pet_repository (PetRepositoryPort): Port adapter for Pet data access.
        """
        self.medical_extractor = medical_extractor
        self.pet_repository = pet_repository

    async def execute(
        self, 
        file_content: bytes, 
        filename: str, 
        file_extractor: FileTextExtractorPort
    ) -> Tuple[Optional[Pet], List[MedicalRecord]]:
        """Executes the data extraction and reconciliation process.

        Args:
            file_content (bytes): The raw byte content of the uploaded document.
            filename (str): The name of the uploaded file.
            file_extractor (FileTextExtractorPort): The injected strategy pattern port 
                used to extract text and entities from the specific file format.

        Returns:
            Tuple[Optional[Pet], List[MedicalRecord]]: A tuple containing the 
                reconciled Pet entity (if found or extracted) and a list of extracted 
                MedicalRecord entities ready for human validation.
        """
        
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