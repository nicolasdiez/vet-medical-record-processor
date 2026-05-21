from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


# --- Value Object DTOs ---

class VitalsDTO(BaseModel):
    """
    DTO for pet vital signs. 
    Decouples the incoming JSON payload from the pure Vitals Value Object in the domain.
    """
    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    temperature_c: Optional[float] = Field(None, description="Temperature in Celsius")
    heart_rate_bpm: Optional[int] = Field(None, description="Heart rate in beats per minute")
    respiratory_rate_bpm: Optional[int] = Field(None, description="Respiratory rate in breaths per minute")


class MedicationDTO(BaseModel):
    """
    DTO for medication details. 
    Handles API validation before data reaches the Medication Value Object.
    """
    name: str = Field(..., description="Name of the medication")
    dosage: str = Field(..., description="Amount and unit of the medication")
    frequency: str = Field(..., description="How often the medication is administered")
    duration: Optional[str] = Field(None, description="How long the treatment lasts")


# --- Pets DTOs ---

class PetCreateDTO(BaseModel):
    """
    DTO used when extracting or creating a new Pet profile. 
    Excludes the 'id' field, as the system is responsible for ID generation.
    """
    name: str
    species: str
    breed: Optional[str] = None


class PetResponse(PetCreateDTO):
    """
    DTO for returning Pet data to the client. 
    Includes the system-generated unique ID.
    """
    id: str


# --- Medical Records DTOs ---

class MedicalRecordCreateDTO(BaseModel):
    """
    DTO for incoming medical record data before persistence.
    """
    date: date
    diagnosis: str
    vitals: Optional[VitalsDTO] = None
    medications: List[MedicationDTO] = Field(default_factory=list)


class MedicalRecordResponse(MedicalRecordCreateDTO):
    """
    DTO for returning a persisted medical record.
    Includes its unique record ID and the foreign key (pet_id) linking it to the patient.
    """
    id: str
    pet_id: str


# --- Clinical Documents DTOs (Phase 1 AI Response) ---

class ProcessDocumentResponse(BaseModel):
    """
    Response payload for Phase 1 (AI Processing). 
    Returns the AI-extracted data as a draft without persisting it, 
    allowing the frontend to render the split-screen UI for human-in-the-loop validation.
    """
    filename: str
    status: str
    message: str
    pet_id: Optional[str] = Field(None, description="Existing Pet ID if found in DB")
    extracted_pet: Optional[PetCreateDTO] = Field(None, description="Pet data extracted by AI")
    extracted_records: List[MedicalRecordCreateDTO] = Field(default_factory=list, description="Records extracted by AI")


# --- Clinical Data DTO (Phase 3 Persistence) ---

class ClinicalDataSaveDTO(BaseModel):
    """
    Payload for Phase 3 (Validation & Persistence). 
    Contains the fully human-validated Pet and Medical Records 
    to be saved atomically in a single database transaction.
    """
    pet: PetResponse
    records: List[MedicalRecordResponse]