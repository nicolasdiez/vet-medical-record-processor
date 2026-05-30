import asyncio
from typing import List, Optional, Tuple

import instructor
from google import genai
from pydantic import BaseModel

from app.domain.entities import MedicalRecord, Pet
from app.domain.ports.outbound.interfaces import MedicalRecordExtractorPort


class ExtractionResponse(BaseModel):
    """Internal Pydantic model for Instructor to structure the LLM output.

    Acts as an aggregation root for the extraction process, ensuring the AI 
    returns data in a predictable schema before mapping to Domain Entities.

    Attributes:
        pet (Optional[Pet]): The extracted pet entity, if found.
        medical_records (List[MedicalRecord]): The extracted list of medical records.
    """
    pet: Optional[Pet] = None
    medical_records: List[MedicalRecord] = []

class LLMGeminiMedicalRecordExtractorAdapter(MedicalRecordExtractorPort):
    """Gemini AI implementation of the MedicalRecordExtractorPort.

    Uses Google's GenAI client and the Instructor library to extract 
    structured clinical data from unstructured text. Offloads the synchronous
    network call to a worker thread to prevent event loop blocking.

    Attributes:
        model_id (str): The specific Gemini model ID used for extraction.
        client (genai.Client): The Google GenAI client instance.
        instructor_client (instructor.Instructor): The wrapped GenAI client for structured outputs.
    """
    def __init__(self, api_key: str, model_id: str):
        """Initializes the adapter with the Gemini API key and model ID.

        Args:
            api_key (str): The secret API key for Google Gemini.
            model_id (str): The target model ID (e.g., 'gemini-2.5-flash').
        """
        self.model_id = model_id
        
        # Initialize the Google GenAI client
        self.client = genai.Client(api_key=api_key)
        
        # Config the instructor
        self.instructor_client = instructor.from_genai(
            client=self.client,
            mode=instructor.Mode.GENAI_STRUCTURED_OUTPUTS,
        )

    # Method naming balanced between generic and specific, to allow more entities
    # to be extracted from the text in the future
    async def extract_entities(self, text: str) -> Tuple[Optional[Pet], List[MedicalRecord]]:
        """Analyzes clinical text and extracts structured entities using Gemini.

        Uses the Instructor library to force the LLM to output a JSON schema 
        that exactly matches our Pydantic domain models.

        Args:
            text (str): The raw unstructured clinical text.

        Returns:
            Tuple[Optional[Pet], List[MedicalRecord]]: The extracted Pet and Records.

        Raises:
            RuntimeError: If the Gemini API fails or validation of the schema fails.
        """
        prompt = (
            "You are an expert veterinary assistant. Extract all clinical information "
            "from the following text. Identify the pet's details and every medical "
            "encounter (diagnosis, vitals, and medications). "
            "CRITICAL: All extracted text values (such as diagnosis, breed, species, "
            "medication names, and clinical instructions) MUST be translated to or "
            "written strictly in Spanish (Castilian). "
            f"Text to process: {text}"
        )

        # Delegate the blocking synchronous network call to a worker thread
        response = await asyncio.to_thread(self._extract_sync, prompt)
        
        return response.pet, response.medical_records
    
    def _extract_sync(self, prompt: str) -> ExtractionResponse:
        """Synchronous worker method that calls the Gemini API via Instructor.

        Args:
            prompt (str): The fully constructed prompt containing instructions and text.

        Returns:
            ExtractionResponse: The structured response matching the Pydantic schema.

        Raises:
            RuntimeError: If the API call fails.
        """
        try:
            response = self.instructor_client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                response_model=ExtractionResponse,
            )
            return response

        except Exception as e:
            raise RuntimeError(f"AI extraction failed: {str(e)}")