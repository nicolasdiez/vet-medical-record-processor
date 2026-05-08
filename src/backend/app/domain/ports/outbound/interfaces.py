from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.entities import Pet, MedicalRecord


class FileTextExtractorPort(ABC):
    """
    Contract for extracting raw text from various file formats (PDF, Word, Images).
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
    async def save(self, pet: Pet) -> Pet:
        pass

    @abstractmethod
    async def get_by_id(self, pet_id: str) -> Optional[Pet]:
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