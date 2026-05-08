from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Vitals(BaseModel):
    """
    Value Object representing the physiological measurements of a Pet 
    during a specific medical encounter. 
    It is strictly immutable because a set of vitals taken at a specific time cannot change.
    """
    model_config = ConfigDict(frozen=True)

    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    temperature_c: Optional[float] = Field(None, description="Temperature in Celsius")
    heart_rate_bpm: Optional[int] = Field(None, description="Heart rate in beats per minute")
    respiratory_rate_bpm: Optional[int] = Field(None, description="Respiratory rate in breaths per minute")

class Medication(BaseModel):
    """
    Value Object representing a prescribed treatment.
    Two medications with the exact same attributes are considered identical.
    """
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Name of the medication")
    dosage: str = Field(..., description="Amount and unit (e.g., '10mg')")
    frequency: str = Field(..., description="Administration frequency (e.g., 'Twice a day')")
    duration: Optional[str] = Field(None, description="Treatment duration (e.g., '7 days')")