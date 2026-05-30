from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

# --- Value Object DTOs ---

class VitalsDTO(BaseModel):
    """Data Transfer Object for pet vital signs.

    Decouples the incoming JSON payload from the pure Vitals Value Object in the domain.

    Attributes:
        weight_kg (Optional[float]): Weight in kilograms.
        temperature_c (Optional[float]): Temperature in Celsius.
        heart_rate_bpm (Optional[int]): Heart rate in beats per minute.
        respiratory_rate_bpm (Optional[int]): Respiratory rate in breaths per minute.
    """
    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    temperature_c: Optional[float] = Field(None, description="Temperature in Celsius")
    heart_rate_bpm: Optional[int] = Field(None, description="Heart rate in beats per minute")
    respiratory_rate_bpm: Optional[int] = Field(None, description="Respiratory rate in breaths per minute")


class MedicationDTO(BaseModel):
    """Data Transfer Object for medication details.

    Handles API validation before data reaches the Medication Value Object.

    Attributes:
        name (str): Name of the medication.
        dosage (str): Amount and unit of the medication.
        frequency (str): How often the medication is administered.
        duration (Optional[str]): How long the treatment lasts.
    """
    name: str = Field(..., description="Name of the medication")
    dosage: str = Field(..., description="Amount and unit of the medication")
    frequency: str = Field(..., description="How often the medication is administered")
    duration: Optional[str] = Field(None, description="How long the treatment lasts")


# --- Pets DTOs ---

class PetCreateDTO(BaseModel):
    """Data Transfer Object for creating or returning a Pet.

    Used at the API boundary to serialize/deserialize Pet data, isolating 
    the external representation from the internal Domain Entity.

    Attributes:
        name (str): The pet's name.
        species (str): The species of the pet.
        breed (Optional[str]): The breed of the pet, if known.
    """
    name: str
    species: str
    breed: Optional[str] = None


class PetResponse(PetCreateDTO):
    """Data Transfer Object for returning Pet data to the client.

    Inherits from PetCreateDTO and includes the system-generated unique ID.

    Attributes:
        id (str): The unique identifier of the pet.
    """
    id: str


# --- Medical Records DTOs ---

class MedicalRecordCreateDTO(BaseModel):
    """Data Transfer Object for creating or returning a Medical Record.

    Includes the patient's data and aggregates complex nested objects 
    (Vitals and Medications).

    Attributes:
        date (date): Date of the clinical encounter.
        diagnosis (str): Veterinarian's unstructured or structured diagnosis notes.
        vitals (Optional[VitalsDTO]): Vitals taken during this specific visit.
        medications (List[MedicationDTO]): Medications prescribed during this visit.
    """
    date: date
    diagnosis: str
    vitals: Optional[VitalsDTO] = None
    medications: List[MedicationDTO] = Field(default_factory=list)


class MedicalRecordResponse(MedicalRecordCreateDTO):
    """Data Transfer Object for returning a persisted medical record.

    Includes its unique record ID and the foreign key (pet_id) linking it to the patient.

    Attributes:
        id (str): The unique identifier of the medical record.
        pet_id (str): The unique identifier of the associated pet.
    """
    id: str
    pet_id: str


# --- Clinical Documents DTOs (Phase 1 AI Response) ---

class ProcessDocumentResponse(BaseModel):
    """Response payload for Phase 1 (AI Processing).

    Returns the AI-extracted data as a draft without persisting it, allowing 
    the frontend to render the split-screen UI for human validation.

    Attributes:
        filename (str): The name of the processed file.
        status (str): The processing status (e.g., 'success').
        message (str): A human-readable result message.
        pet_id (Optional[str]): Existing Pet ID if found in DB.
        extracted_pet (Optional[PetCreateDTO]): Pet data extracted by AI.
        extracted_records (List[MedicalRecordCreateDTO]): Records extracted by AI.
    """
    filename: str
    status: str
    message: str
    pet_id: Optional[str] = Field(None, description="Existing Pet ID if found in DB")
    extracted_pet: Optional[PetCreateDTO] = Field(None, description="Pet data extracted by AI")
    extracted_records: List[MedicalRecordCreateDTO] = Field(default_factory=list, description="Records extracted by AI")


# --- Clinical Data DTO (Phase 3 Persistence) ---

class ClinicalDataSaveDTO(BaseModel):
    """Payload for Phase 3 (Validation & Persistence).

    Contains the fully human-validated Pet and Medical Records 
    to be saved atomically in a single database transaction.

    Attributes:
        pet (PetResponse): The validated pet data.
        records (List[MedicalRecordResponse]): The validated list of medical records.
    """
    pet: PetResponse
    records: List[MedicalRecordResponse]