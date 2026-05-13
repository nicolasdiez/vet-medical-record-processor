from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from typing import List

from app.domain.entities import Pet, MedicalRecord
from app.application.use_cases.extract_clinical_data import ExtractClinicalDataUseCase
from app.application.use_cases.save_clinical_data import SaveClinicalDataUseCase
from app.infrastructure.outbound.pdf_text_extractor import PDFFileTextExtractorAdapter
from .schemas import (
    ProcessDocumentResponse, PetCreateDTO, 
    MedicalRecordCreateDTO, MedicalRecordResponse, ClinicalDataSaveDTO
)
from app.application.use_cases.get_pet_clinical_history import GetPetClinicalHistoryUseCase

# ---------------------------------------------------------
# FastAPI Dependency Injection Mechanism - Placeholders (Implemented in main.py)
# ---------------------------------------------------------
async def get_extract_use_case() -> ExtractClinicalDataUseCase:
    raise NotImplementedError()

async def get_save_use_case() -> SaveClinicalDataUseCase:
    raise NotImplementedError()

async def get_history_use_case() -> GetPetClinicalHistoryUseCase:
    raise NotImplementedError()

# ---------------------------------------------------------
# Router 1: Clinical Documents (Phase 1: AI Processing)
# ---------------------------------------------------------
documents_router = APIRouter(prefix="/api/v1/clinical-documents", tags=["Clinical Documents"])

@documents_router.post(
    "/process", 
    response_model=ProcessDocumentResponse,
    summary="Process a clinical document (No persistence)"
)
async def process_document(
    file: UploadFile = File(...),
    use_case: ExtractClinicalDataUseCase = Depends(get_extract_use_case)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Strategy Pattern: Inject the correct extractor adapter
    if file.content_type == "application/pdf":
        extractor = PDFFileTextExtractorAdapter()
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    file_content = await file.read()

    try:
        # Execute the Application layer Use Case
        domain_pet, domain_records = await use_case.execute(file_content, file.filename, extractor)
        
        # Map Domain Entities back to DTOs for the response
        pet_dto = None
        pet_id = None
        if domain_pet:
            pet_id = domain_pet.id
            pet_dto = PetCreateDTO(**domain_pet.model_dump())
            
        records_dto = [MedicalRecordCreateDTO(**rec.model_dump()) for rec in domain_records]

        return ProcessDocumentResponse(
            filename=file.filename,
            status="processed",
            message="Document analyzed successfully. Waiting for human validation.",
            pet_id=pet_id,
            extracted_pet=pet_dto,
            extracted_records=records_dto
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# Router 2: Clinical Data (Phase 3: Persistence)
# ---------------------------------------------------------
clinical_data_router = APIRouter(prefix="/api/v1/clinical-data", tags=["Clinical Data Persistence"])

@clinical_data_router.post(
    "", 
    status_code=status.HTTP_201_CREATED,
    summary="Atomically save validated Pet and Medical Records"
)
async def save_clinical_data(
    payload: ClinicalDataSaveDTO,
    use_case: SaveClinicalDataUseCase = Depends(get_save_use_case)
):
    """
    Phase 3 of the Human-in-the-Loop flow: Persistence.
    Receives the unified, human-corrected payload and persists it atomically.
    """
    try:
        # Map DTOs back to Domain Entities
        domain_pet = Pet(**payload.pet.model_dump())
        domain_records = [MedicalRecord(**rec.model_dump()) for rec in payload.records]
        
        # Execute the Use Case (Handles the DB transaction commit/rollback)
        await use_case.execute(domain_pet, domain_records)
        
        return {"message": "Clinical data successfully persisted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# Router 3: Pet History (For GET requests)
# ---------------------------------------------------------
pets_router = APIRouter(prefix="/api/v1/pets", tags=["Pets History"])

@pets_router.get(
    "/{pet_id}/medical-records", 
    response_model=List[MedicalRecordResponse],
    summary="Retrieve full clinical history"
)
async def list_pet_medical_records(
    pet_id: str,
    use_case: GetPetClinicalHistoryUseCase = Depends(get_history_use_case)
):
    """
    Retrieves the complete clinical history (all medical records) associated 
    with a specific pet. Used by the frontend to display the patient's timeline.
    """
    try:
        domain_records = await use_case.execute(pet_id)
        
        # Map domain entities to DTOs
        return [MedicalRecordResponse(**rec.model_dump()) for rec in domain_records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))