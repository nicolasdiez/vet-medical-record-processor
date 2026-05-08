from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List
from datetime import date
from .schemas import (
    ProcessDocumentResponse, PetResponse, PetCreateDTO, 
    MedicalRecordResponse, MedicalRecordCreateDTO
)

# ---------------------------------------------------------
# Router 1: Clinical Documents (Phase 1: AI Processing)
# ---------------------------------------------------------
documents_router = APIRouter(prefix="/api/v1/clinical-documents", tags=["Clinical Documents"])

@documents_router.post(
    "/process", 
    response_model=ProcessDocumentResponse,
    summary="Process a clinical document (No persistence)"
)
async def process_document(file: UploadFile = File(...)):
    """
    Phase 1 of the Human-in-the-Loop flow: AI Processing.
    
    This endpoint receives a clinical document (e.g., PDF, Image), extracts the 
    raw text using an OCR/PDF parser, and utilizes an LLM to map the unstructured 
    medical jargon into structured domain entities (Pet and MedicalRecords).
    
    CRITICAL: This endpoint does NOT persist data to the database. It returns 
    the extracted data payload so the frontend can display it in a split-screen 
    UI for human validation and editing.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
        
    # TODO: Pass the file to the Application Layer (ProcessRecordUseCase) here.
    # The following is a mock response to simulate the AI extraction output.
    return ProcessDocumentResponse(
        filename=file.filename,
        status="processed",
        message="Document analyzed successfully. Waiting for human validation.",
        pet_id=None, # Indicates a new pet scenario (not found in DB)
        extracted_pet=PetCreateDTO(name="Max", species="Dog", breed="Golden Retriever"),
        extracted_records=[
            MedicalRecordCreateDTO(
                date=date.today(),
                diagnosis="Routine checkup, healthy. No abnormalities detected.",
                medications=[]
            )
        ]
    )

# ---------------------------------------------------------
# Router 2: Pets & Medical Records (Phase 3: Persistence)
# ---------------------------------------------------------
pets_router = APIRouter(prefix="/api/v1/pets", tags=["Pets & Medical Records"])

@pets_router.post(
    "", 
    response_model=PetResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Pet"
)
async def create_pet(pet_in: PetCreateDTO): 
    """
    Phase 3 of the Human-in-the-Loop flow: Persistence.
    
    Creates a new Pet entity in the database. This endpoint is called by the 
    frontend ONLY after the veterinarian has reviewed and approved the AI-extracted 
    data. The database will generate and return the unique Pet ID.
    """
    # TODO: Pass to Application Layer / Repository to execute INSERT
    # Mocking the DB insertion response:
    return PetResponse(id="new_pet_123", **pet_in.model_dump())

@pets_router.put(
    "/{pet_id}", 
    response_model=PetResponse,
    summary="Update an existing Pet"
)
async def update_pet(pet_id: str, pet_in: PetCreateDTO):
    """
    Phase 3 of the Human-in-the-Loop flow: Persistence (Update).
    
    Updates an existing Pet entity in the database. Used when the AI correctly 
    identified an existing pet, but the user made manual corrections to its static 
    information (e.g., fixing a typo in the breed) during the review phase.
    """
    # TODO: Pass to Application Layer / Repository to execute UPDATE
    return PetResponse(id=pet_id, **pet_in.model_dump())

@pets_router.post(
    "/{pet_id}/medical-records", 
    response_model=List[MedicalRecordResponse], 
    status_code=status.HTTP_201_CREATED,
    summary="Persist validated medical records"
)
async def create_medical_records(pet_id: str, records_in: List[MedicalRecordCreateDTO]):
    """
    Phase 3 of the Human-in-the-Loop flow: Persistence.
    
    Persists a list of medical records (including their value objects like Vitals 
    and Medications) associated with a specific pet. Called after the user has 
    validated the extracted diagnoses.
    """
    # TODO: Pass to Application Layer / Repository to execute INSERT
    # Mocking the DB insertion response:
    return [
        MedicalRecordResponse(id=f"rec_{i}", pet_id=pet_id, **rec.model_dump()) 
        for i, rec in enumerate(records_in)
    ]

@pets_router.get(
    "/{pet_id}/medical-records", 
    response_model=List[MedicalRecordResponse],
    summary="Retrieve full clinical history"
)
async def list_pet_medical_records(pet_id: str):
    """
    Retrieves the complete clinical history (all medical records) associated 
    with a specific pet. Used by the frontend to display the patient's timeline.
    """
    # TODO: Fetch from Application Layer / Repository
    return []