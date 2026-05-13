from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Pet
from app.domain.ports.outbound.interfaces import PetRepositoryPort
from app.infrastructure.outbound.persistence.models import PetORM


class SQLPetRepositoryAdapter(PetRepositoryPort):
    """
    SQLAlchemy implementation of the PetRepositoryPort.
    Handles persistence and retrieval of Pet entities from the database.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, pet: Pet) -> None:
        """
        Inserts a new pet or updates an existing one using an upsert (merge).
        """
        pet_orm = PetORM(
            id=str(pet.id),
            name=pet.name,
            species=pet.species,
            breed=pet.breed
        )
        # merge() performs an upsert (INSERT if new, UPDATE if id exists)
        await self.session.merge(pet_orm)

    async def get_by_id(self, pet_id: str) -> Optional[Pet]:
        """
        Retrieves a pet by its unique identifier.
        """
        stmt = select(PetORM).where(PetORM.id == pet_id)
        result = await self.session.execute(stmt)
        orm_pet = result.scalar_one_or_none()

        if not orm_pet:
            return None

        return Pet(
            id=orm_pet.id,
            name=orm_pet.name,
            species=orm_pet.species,
            breed=orm_pet.breed
        )

    async def find_by_name_and_species(self, name: str, species: str) -> Optional[Pet]:
        """
        Finds a pet by its name and species (used in Phase 1 to check for existing pets).
        Uses case-insensitive matching.
        """
        stmt = select(PetORM).where(
            PetORM.name.ilike(name),
            PetORM.species.ilike(species)
        )
        result = await self.session.execute(stmt)
        orm_pet = result.scalar_one_or_none()

        if not orm_pet:
            return None

        return Pet(
            id=orm_pet.id,
            name=orm_pet.name,
            species=orm_pet.species,
            breed=orm_pet.breed
        )