from typing import List, Optional, Tuple

import instructor
from google import genai
from pydantic import BaseModel

from app.domain.entities import MedicalRecord, Pet
from app.domain.ports.outbound.interfaces import MedicalRecordExtractorPort


class ExtractionResponse(BaseModel):
    pet: Optional[Pet] = None
    medical_records: List[MedicalRecord] = []

class LLMGeminiMedicalRecordExtractorAdapter(MedicalRecordExtractorPort):
    def __init__(self, api_key: str, model_id: str):
        self.model_id = model_id
        
        # Initialize the modern Google GenAI client
        self.client = genai.Client(api_key=api_key)
        
        # Config the instructor
        self.instructor_client = instructor.from_genai(
            client=self.client,
            mode=instructor.Mode.GENAI_STRUCTURED_OUTPUTS,
        )

    # Method naming balanced between generic and specific, to allow more entities
    # to be extracted from the text in the future
    async def extract_entities(self, text: str) -> Tuple[Optional[Pet], List[MedicalRecord]]:
        prompt = (
            "You are an expert veterinary assistant. Extract all clinical information "
            "from the following text. Identify the pet's details and every medical "
            "encounter (diagnosis, vitals, and medications). "
            "CRITICAL: All extracted text values (such as diagnosis, breed, species, "
            "medication names, and clinical instructions) MUST be translated to or "
            "written strictly in Spanish (Castilian). "
            f"Text to process: {text}"
        )

        try:
            response = self.instructor_client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                response_model=ExtractionResponse,
            )
            return response.pet, response.medical_records

        except Exception as e:
            raise RuntimeError(f"AI extraction failed: {str(e)}")