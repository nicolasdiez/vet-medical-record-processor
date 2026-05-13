from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from app.domain.entities import Pet, MedicalRecord
from app.domain.ports.outbound.interfaces import FileTextExtractorPort

class ExtractClinicalDataUseCasePort(ABC):
    """
    Inbound port for Phase 1: Processing a raw document and extracting data.
    It returns the draft data for user review. It does NOT persist anything.
    """
    
    @abstractmethod
    async def execute(self, file_content: bytes, file_extractor: FileTextExtractorPort) -> Tuple[Optional[Pet], List[MedicalRecord]]:
        pass


class SaveClinicalDataUseCasePort(ABC):
    """
    Inbound port for Phase 3: Persisting the data after human confirmation.
    Receives the exact entities (potentially modified by the user) and saves them to the DB.
    """
    
    @abstractmethod
    async def execute(self, pet: Pet, records: List[MedicalRecord]) -> None:
        pass


class GetPetClinicalHistoryUseCasePort(ABC):
    """
    Inbound port for retrieving a pet's complete medical history.
    """
    @abstractmethod
    async def execute(self, pet_id: str) -> List[MedicalRecord]:
        pass