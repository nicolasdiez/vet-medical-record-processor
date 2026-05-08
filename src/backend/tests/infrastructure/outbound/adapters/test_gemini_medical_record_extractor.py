import pytest
import os
from dotenv import load_dotenv
from app.infrastructure.outbound.adapters.gemini_medical_record_extractor import LLMGeminiMedicalRecordExtractorAdapter
from app.domain.entities import Pet, MedicalRecord
from app.config import settings

# Load environment variables for the test context
load_dotenv(".env.dev")

@pytest.fixture
def api_key() -> str:
    """
    Retrieves the API key from the environment. 
    Skips the test if the key is not present to prevent CI/CD failures.
    """
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        pytest.skip("GEMINI_API_KEY not found in .env.dev. Skipping real LLM integration test.")
    return key

@pytest.fixture
def extractor(api_key: str) -> LLMGeminiMedicalRecordExtractorAdapter:
    """
    Instantiates the adapter using the model configured in the environment settings.
    """
    return LLMGeminiMedicalRecordExtractorAdapter(
        api_key=api_key, 
        model_id=settings.GEMINI_MODEL
    )

@pytest.mark.asyncio
async def test_extract_entities_with_real_llm(extractor: LLMGeminiMedicalRecordExtractorAdapter):
    """
    Integration test that sends a controlled clinical text to the actual Gemini API
    and validates that Instructor successfully maps the response into our Pydantic domain models.
    """
    # Controlled input text simulating a short clinical note
    sample_clinical_text = (
        "Patient: Bella, a 5-year-old Golden Retriever (Dog). "
        "Date of visit: 2023-10-25. "
        "Vitals taken: Weight is 28.5 kg, Temperature 38.5 C. "
        "Diagnosis: Mild ear infection in the left ear. "
        "Treatment prescribed: Otomax ear drops, apply 3 drops twice a day for 7 days."
    )

    # Execute the method under test
    pet, records = await extractor.extract_entities(sample_clinical_text)

    # 1. Validate Pet Entity
    assert pet is not None
    assert isinstance(pet, Pet)
    assert pet.name == "Bella"
    assert pet.species.lower() == "dog"
    assert pet.breed is not None and "retriever" in pet.breed.lower()

    # 2. Validate MedicalRecord Entity List
    assert isinstance(records, list)
    assert len(records) == 1
    
    record = records[0]
    assert isinstance(record, MedicalRecord)
    assert str(record.date) == "2023-10-25"
    assert "ear infection" in record.diagnosis.lower()

    # 3. Validate Vitals Value Object
    assert record.vitals is not None
    assert record.vitals.weight_kg == 28.5
    assert record.vitals.temperature_c == 38.5

    # 4. Validate Medication Value Object
    assert len(record.medications) == 1
    med = record.medications[0]
    assert "Otomax" in med.name
    assert "3 drops" in med.dosage.lower()
    assert "twice" in med.frequency.lower()
    assert "7 days" in med.duration.lower()