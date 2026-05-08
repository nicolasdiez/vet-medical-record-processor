from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

# Import our strictly immutable Value Objects
from .value_objects import Vitals, Medication

class Pet(BaseModel):
    """
    Entity representing the animal patient.
    Defined by its unique identity (id), not just its attributes.
    """
    id: str = Field(..., description="Unique identifier for the pet")
    name: str = Field(..., description="Name of the pet")
    species: str = Field(..., description="Species (e.g., Dog, Cat)")
    breed: Optional[str] = Field(None, description="Specific breed of the animal")

class MedicalRecord(BaseModel):
    """
    Entity representing an individual clinical encounter or diagnosis.
    It is uniquely identifiable, belongs to a specific Pet, and aggregates Value Objects.
    """
    id: str = Field(..., description="Unique identifier for the medical record")
    pet_id: str = Field(..., description="Identifier of the associated Pet (Foreign Key concept)")
    date: datetime.date = Field(..., description="Date of the clinical encounter")
    diagnosis: str = Field(..., description="Veterinarian's unstructured or structured diagnosis notes")
    
    # Composition: Aggregating our Value Objects
    vitals: Optional[Vitals] = Field(None, description="Vitals taken during this specific visit")
    medications: List[Medication] = Field(default_factory=list, description="Medications prescribed during this visit")