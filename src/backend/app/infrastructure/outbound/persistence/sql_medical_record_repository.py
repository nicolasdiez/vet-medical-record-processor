from datetime import date
from typing import Any, List, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import MedicalRecord, Medication, Vitals
from app.domain.ports.outbound.interfaces import MedicalRecordRepositoryPort
from app.infrastructure.outbound.persistence.models import MedicalRecordORM


class SQLMedicalRecordRepositoryAdapter(MedicalRecordRepositoryPort):
    """SQLAlchemy implementation of the MedicalRecordRepositoryPort.

    Handles the translation between pure domain entities and ORM models, including
    the serialization and deserialization of Value Objects into JSON.

    Attributes:
        session (AsyncSession): The active database session.
    """
    
    def __init__(self, session: AsyncSession):
        """Initializes the adapter with a database session.

        Args:
            session (AsyncSession): The SQLAlchemy async session to use.
        """
        self.session = session

    async def save_bulk(self, records: List[MedicalRecord]) -> None:
        """Saves or updates a list of medical records in the database.

        Serializes internal Value Objects (like Vitals and Medications) into 
        dictionaries so they can be stored in JSON columns.

        Args:
            records (List[MedicalRecord]): The list of domain records to persist.
        """
        for record in records:
            # Serialize Value Objects to dictionaries for JSON columns
            vitals_dict = record.vitals.model_dump() if record.vitals else None
            meds_list = [med.model_dump() for med in record.medications] if record.medications else []

            record_orm = MedicalRecordORM(
                id=str(record.id),
                pet_id=str(record.pet_id),
                date=record.date,
                diagnosis=cast(str, record.diagnosis),
                vitals=vitals_dict,
                medications=meds_list
            )
            # merge() performs an upsert (INSERT if new, UPDATE if id exists)
            await self.session.merge(record_orm)

    async def get_by_pet_id(self, pet_id: str) -> List[MedicalRecord]:
        """Retrieves the complete clinical history for a specific pet.

        Queries the database and reconstructs the pure Domain Entities, 
        including parsing JSON columns back into Value Objects.

        Args:
            pet_id (str): The unique identifier of the pet.

        Returns:
            List[MedicalRecord]: The list of medical records associated with the pet.
        """
        stmt = select(MedicalRecordORM).where(MedicalRecordORM.pet_id == pet_id)
        result = await self.session.execute(stmt)
        orm_records = result.scalars().all()

        domain_records = []
        for orm in orm_records:
            # Reconstruct Value Objects from JSON dictionaries
            vitals = Vitals(**orm.vitals) if orm.vitals else None
            medications = [Medication(**med) for med in cast(list[Any], orm.medications)] if orm.medications else []

            domain_record = MedicalRecord(
                id=cast(str, orm.id),
                pet_id=cast(str, orm.pet_id),
                date=cast(date, orm.date),
                diagnosis=cast(str, orm.diagnosis),
                vitals=vitals,
                medications=medications
            )
            domain_records.append(domain_record)

        return domain_records