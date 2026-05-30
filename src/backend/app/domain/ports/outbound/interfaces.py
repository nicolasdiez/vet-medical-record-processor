from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from app.domain.entities import MedicalRecord, Pet


class FileTextExtractorPort(ABC):
    """Contract for extracting raw clinical text from various file formats.

    Defines how adapters should extract plain text from PDFs, Word docs, or images.
    """
    @abstractmethod
    async def extract_text(self, file_content: bytes, filename: str) -> str:
        """Extracts text from the given binary file content.

        Args:
            file_content (bytes): The raw binary content of the file.

        Returns:
            str: The extracted plain text.

        Raises:
            ValueError: If the file format is unsupported or extraction fails.
        """
        pass

class MedicalRecordExtractorPort(ABC):
    """Outbound port for extracting structured entities from clinical text.

    Defines the contract for adapters (like LLMs) that parse unstructured 
    veterinary notes and map them into pure Domain Entities.
    """
    @abstractmethod
    async def extract_entities(self, text: str) -> Tuple[Optional[Pet], List[MedicalRecord]]:
        """Analyzes clinical text and extracts Pet and MedicalRecord entities.

        Args:
            text (str): The unstructured clinical text extracted from a document.

        Returns:
            Tuple[Optional[Pet], List[MedicalRecord]]: A tuple containing the extracted 
                Pet (if any) and a list of identified Medical Records.

        Raises:
            RuntimeError: If the underlying extraction service (e.g., AI model) fails.
        """
        pass

class PetRepositoryPort(ABC):
    """
    Outbound port for persisting and retrieving Pet entities.
    """
    
    @abstractmethod
    async def save(self, pet: Pet) -> None:
        """Saves a new pet or updates an existing one in the database.

        Args:
            pet (Pet): The Pet domain entity to persist.
        """
        pass

    @abstractmethod
    async def get_by_id(self, pet_id: str) -> Optional[Pet]:
        """
        Retrieves a pet by its unique identifier.

         Args:
            pet (Pet): The Pet domain entity to retrieve.
        """
        pass

    @abstractmethod
    async def find_by_name_and_species(self, name: str, species: str) -> Optional[Pet]:
        """Finds a pet by its name and species (used to check for existing pets).

        Args:
            name (str): The name of the pet.
            species (str): The species of the pet.

        Returns:
            Optional[Pet]: The Pet entity if found, None otherwise.
        """
        pass

class MedicalRecordRepositoryPort(ABC):
    """
    Outbound port for persisting and retrieving MedicalRecord entities.
    """
    @abstractmethod
    async def save_bulk(self, records: List[MedicalRecord]) -> None:
        """Saves or updates a list of medical records in the database.

        Args:
            records (List[MedicalRecord]): The list of medical records to persist.
        """
        pass

    @abstractmethod
    async def get_by_pet_id(self, pet_id: str) -> List[MedicalRecord]:
        """Retrieves the complete clinical history for a specific pet.

        Args:
            pet_id (str): The unique identifier of the pet.

        Returns:
            List[MedicalRecord]: A list of all medical records associated with the pet.
        """
        pass