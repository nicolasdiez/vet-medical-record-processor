from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# --- Value Object DTOs ---

class VitalsDTO(BaseModel):
    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    temperature_c: Optional[float] = Field(None, description="Temperature in Celsius")
    heart_rate_bpm: Optional[int] = Field(None, description="Heart rate in beats per minute")
    respiratory_rate_bpm: Optional[int] = Field(None, description="Respiratory rate in breaths per minute")

class MedicationDTO(BaseModel):
    name: str = Field(..., description="Name of the medication")
    dosage: str = Field(..., description="Amount and unit of the medication")
    frequency: str = Field(..., description="How often the medication is administered")
    duration: Optional[str] = Field(None, description="How long the treatment lasts")

# --- Pets DTOs ---

class PetCreateDTO(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None

class PetResponse(PetCreateDTO):
    id: str

# --- Medical Records DTOs ---

class MedicalRecordCreateDTO(BaseModel):
    date: date
    diagnosis: str
    vitals: Optional[VitalsDTO] = None
    medications: List[MedicationDTO] = Field(default_factory=list)

class MedicalRecordResponse(MedicalRecordCreateDTO):
    id: str
    pet_id: str

# --- Clinical Documents DTOs (Phase 1 AI Response) ---

class ProcessDocumentResponse(BaseModel):
    filename: str
    status: str
    message: str
    pet_id: Optional[str] = Field(None, description="Existing Pet ID if found in DB")
    extracted_pet: Optional[PetCreateDTO] = Field(None, description="Pet data extracted by AI")
    extracted_records: List[MedicalRecordCreateDTO] = Field(default_factory=list, description="Records extracted by AI")