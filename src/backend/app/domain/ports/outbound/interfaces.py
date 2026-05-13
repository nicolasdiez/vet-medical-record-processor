from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.entities import Pet, MedicalRecord


class FileTextExtractorPort(ABC):
    """
    Contract for extracting raw clinical text from various file formats (PDF, Word, Images).
    """
    @abstractmethod
    async def extract_text(self, file_content: bytes, filename: str) -> str:
        pass

class MedicalRecordExtractorPort(ABC):
    """
    Contract for analyzing raw clinical text to extract domain entities.
    It processes the full document text to avoid breaking context across visits.
    """
    @abstractmethod
    async def extract_entities(self, text: str) -> Tuple[Optional[Pet], List[MedicalRecord]]:
        pass

class PetRepositoryPort(ABC):
    """
    Contract for persisting and retrieving Pet entities.
    """
    
    @abstractmethod
    async def save(self, pet: Pet) -> None:
        """
        Inserts a new pet or updates an existing one.
        """
        pass

    @abstractmethod
    async def get_by_id(self, pet_id: str) -> Optional[Pet]:
        """
        Retrieves a pet by its unique identifier.
        """
        pass

    @abstractmethod
    async def find_by_name_and_species(self, name: str, species: str) -> Optional[Pet]:
        """
        Finds a pet by its name and species (used in Phase 1 to check for existing pets).
        """
        pass

class MedicalRecordRepositoryPort(ABC):
    """
    Contract for persisting and retrieving MedicalRecord entities.
    """
    @abstractmethod
    async def save_bulk(self, records: List[MedicalRecord]) -> List[MedicalRecord]:
        pass

    @abstractmethod
    async def get_by_pet_id(self, pet_id: str) -> List[MedicalRecord]:
        """
        Retrieves the complete clinical history for a specific pet.
        """
        pass