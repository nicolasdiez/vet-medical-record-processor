from sqlalchemy import JSON, Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship

from app.infrastructure.outbound.persistence.database import Base


class PetORM(Base):
    """SQLAlchemy ORM model for the pets table.

    Maps the pure Pet domain entity to the relational database schema.

    Attributes:
        id (Column): Primary key, unique identifier for the pet (String).
        name (Column): The name of the pet (String).
        species (Column): The species of the pet (String).
        breed (Column): The breed of the pet, if known (String, nullable).
        records (relationship): One-to-many relationship with MedicalRecordORM.
    """
    __tablename__ = "pets"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=True)

    # Relationship to MedicalRecordORM
    records = relationship("MedicalRecordORM", back_populates="pet", cascade="all, delete-orphan")


class MedicalRecordORM(Base):
    """SQLAlchemy ORM model for the medical_records table.

    Maps the pure MedicalRecord domain entity to the relational database schema, 
    storing Value Objects as JSON columns.

    Attributes:
        id (Column): Primary key, unique identifier for the medical record (String).
        pet_id (Column): Foreign key linking to the associated pet (String).
        date (Column): Date of the clinical encounter (Date).
        diagnosis (Column): Veterinarian's diagnosis notes (String).
        vitals (Column): JSON column storing the Vitals value object.
        medications (Column): JSON column storing the list of Medication value objects.
        pet (relationship): Many-to-one relationship with PetORM.
    """
    __tablename__ = "medical_records"

    id = Column(String, primary_key=True, index=True)
    pet_id = Column(String, ForeignKey("pets.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    diagnosis = Column(String, nullable=False)
    
    # Store complex Value Objects as JSON structures
    vitals = Column(JSON, nullable=True)
    medications = Column(JSON, nullable=True)

    # Relationship to PetORM
    pet = relationship("PetORM", back_populates="records")