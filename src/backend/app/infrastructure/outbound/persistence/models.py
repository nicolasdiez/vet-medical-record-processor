from sqlalchemy import Column, String, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.infrastructure.outbound.persistence.database import Base

class PetORM(Base):
    """
    SQLAlchemy ORM model for the 'pets' table.
    """
    __tablename__ = "pets"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=True)

    # Relationship to MedicalRecordORM
    records = relationship("MedicalRecordORM", back_populates="pet", cascade="all, delete-orphan")


class MedicalRecordORM(Base):
    """
    SQLAlchemy ORM model for the 'medical_records' table.
    Value objects (vitals, medications) are stored as JSON for simplicity in the MVP.
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