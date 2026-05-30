from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Vitals(BaseModel):
    """Value Object representing physiological measurements during a visit.

    It is strictly immutable because a set of vitals taken at a specific time cannot change.

    Attributes:
        weight_kg (Optional[float]): Weight in kilograms.
        temperature_c (Optional[float]): Temperature in Celsius.
        heart_rate_bpm (Optional[int]): Heart rate in beats per minute.
        respiratory_rate_bpm (Optional[int]): Respiratory rate in breaths per minute.
    """
    model_config = ConfigDict(frozen=True)

    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    temperature_c: Optional[float] = Field(None, description="Temperature in Celsius")
    heart_rate_bpm: Optional[int] = Field(None, description="Heart rate in beats per minute")
    respiratory_rate_bpm: Optional[int] = Field(None, description="Respiratory rate in breaths per minute")

class Medication(BaseModel):
    """Value Object representing a prescribed medication.

    It is strictly immutable and forms part of a Medical Record.
    Two medications with the exact same attributes are considered identical.

    Attributes:
        name (str): Name of the medication.
        dosage (str): Amount and unit (e.g., '10mg').
        frequency (str): Administration frequency (e.g., 'Twice a day').
        duration (Optional[str]): Treatment duration (e.g., '7 days').
    """
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Name of the medication")
    dosage: str = Field(..., description="Amount and unit (e.g., '10mg')")
    frequency: str = Field(..., description="Administration frequency (e.g., 'Twice a day')")
    duration: Optional[str] = Field(None, description="Treatment duration (e.g., '7 days')")