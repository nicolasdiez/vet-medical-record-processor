import os
import uuid
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import date

from app.main import app
from app.domain.entities import Pet, MedicalRecord

# UUIDs for the mock entities
mock_pet_id = str(uuid.uuid4())
mock_record_id = str(uuid.uuid4())

# Random pet name so the test can be executed in isolation every time (no collisions in DB)
unique_name = f"Rex_{mock_pet_id[:8]}"

# Create entities
mock_pet = Pet(id=mock_pet_id, name=unique_name, species="Dog", breed="Labrador")
mock_record = MedicalRecord(id=mock_record_id, pet_id=mock_pet_id, date=date.today(), diagnosis="Healthy dog")

# Using FastAPI TestClient which wraps the async routes to make them sync (blocking).
# Because the test method does not use await functions, the test method does not need async decorator 
def test_full_clinical_flow_e2e():
    """
    Tests the complete happy path:
    1. Upload PDF (using a real fixture, mocking only the LLM)
    2. Save the validated data to the SQLite DB
    3. Retrieve the clinical history from the DB
    """
    with TestClient(app) as client:
        
        # --- 1. HEALTH CHECK ---
        resp_health = client.get("/health")
        assert resp_health.status_code == 200

        # --- 2. PHASE 1: PROCESS DOCUMENT ---
        target_mock = "app.infrastructure.outbound.gemini_medical_record_extractor.LLMGeminiMedicalRecordExtractorAdapter.extract_entities"
        
        with patch(target_mock) as mock_extract:
            mock_extract.return_value = (mock_pet, [mock_record])
            
            # Use the real PDF fixture so the PDFTextExtractorAdapter doesn't crash
            # Path is relative to where pytest is executed (src/backend)
            fixture_path = Path("tests/fixtures/clinical_history_1.pdf")
            
            # Ensure the fixture exists before testing
            assert fixture_path.exists(), f"Fixture not found at {fixture_path.absolute()}"
            
            with open(fixture_path, "rb") as pdf_file:
                files = {"file": ("clinical_history_1.pdf", pdf_file, "application/pdf")}
                resp_process = client.post("/api/v1/clinical-documents/process", files=files)
            
            assert resp_process.status_code == 200, resp_process.text
            process_data = resp_process.json()
            assert process_data["extracted_pet"]["name"] == unique_name
            
        # --- 3. PHASE 3: SAVE CLINICAL DATA ---
        payload = {
            "pet": {
                "id": str(mock_pet.id), 
                "name": unique_name, 
                "species": "Dog", 
                "breed": "Labrador"
            },
            "records": [
                {
                    "id": str(mock_record.id), 
                    "pet_id": str(mock_pet.id), 
                    "date": str(date.today()), 
                    "diagnosis": "Healthy dog",
                    "medications": []
                }
            ]
        }
        
        resp_save = client.post("/api/v1/clinical-data", json=payload)
        assert resp_save.status_code == 201
        assert resp_save.json()["message"] == "Clinical data successfully persisted."

        # --- 4. GET HISTORY ---
        resp_get = client.get(f"/api/v1/pets/{mock_pet.id}/medical-records")
        assert resp_get.status_code == 200
        
        history_data = resp_get.json()
        assert len(history_data) == 1
        assert history_data[0]["diagnosis"] == "Healthy dog"
        assert history_data[0]["pet_id"] == str(mock_pet.id)