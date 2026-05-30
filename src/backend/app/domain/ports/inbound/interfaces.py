from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from app.domain.entities import MedicalRecord, Pet
from app.domain.ports.outbound.interfaces import FileTextExtractorPort


class ExtractClinicalDataUseCasePort(ABC):
    """Inbound port for Phase 1: AI Processing and text extraction.
    
    Defines the contract for the application service that coordinates the extraction 
    of clinical text from raw files and maps them to domain entities.
    """
    
    @abstractmethod
    async def execute(
        self, 
        file_content: bytes, 
        filename: str, 
        file_extractor: FileTextExtractorPort
    ) -> Tuple[Optional[Pet], List[MedicalRecord]]:
        """Processes a raw file to extract a Pet and its Medical Records.

        Args:
            file_content (bytes): The raw binary content of the file.
            filename (str): The name of the file (including extension).
            file_extractor (FileTextExtractorPort): The strategy to parse the file.

        Returns:
            Tuple[Optional[Pet], List[MedicalRecord]]: The extracted domain entities.
        """
        pass

class SaveClinicalDataUseCasePort(ABC):
    """Inbound port for Phase 3: Persisting the data after human confirmation.

    Defines the contract for the application service responsible for saving 
    validated clinical entities into the database atomically.
    """
    
    @abstractmethod
    async def execute(self, pet: Pet, records: List[MedicalRecord]) -> None:
        """Saves a pet and its associated medical records to the database.

        Args:
            pet (Pet): The verified Pet domain entity to be saved or updated.
            records (List[MedicalRecord]): The verified list of medical records.

        Raises:
            Exception: If the underlying persistence transaction fails.
        """
        pass

class GetPetClinicalHistoryUseCasePort(ABC):
    """Inbound port for retrieving a pet's complete medical history.

    Defines the contract for the application service that fetches all historical 
    clinical records for a given patient.
    """
    @abstractmethod
    async def execute(self, pet_id: str) -> List[MedicalRecord]:
        """Retrieves all medical records associated with a specific pet ID.

        Args:
            pet_id (str): The unique identifier of the pet.

        Returns:
            List[MedicalRecord]: A chronological list of the pet's medical records.
        """
        pass