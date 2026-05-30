from typing import Optional, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Pet
from app.domain.ports.outbound.interfaces import PetRepositoryPort
from app.infrastructure.outbound.persistence.models import PetORM


class SQLPetRepositoryAdapter(PetRepositoryPort):
    """SQLAlchemy implementation of the PetRepositoryPort.

    Handles the translation between pure domain entities and ORM models.

    Attributes:
        session (AsyncSession): The active database session.
    """

    def __init__(self, session: AsyncSession):
        """Initializes the adapter with a database session.

        Args:
            session (AsyncSession): The SQLAlchemy async session to use.
        """
        self.session = session

    async def save(self, pet: Pet) -> None:
        """Inserts a new pet or updates an existing one using an upsert (merge).

        Args:
            pet (Pet): The Pet domain entity to persist.
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
        """Retrieves a pet by its unique identifier.

        Args:
            pet_id (str): The unique ID of the pet.

        Returns:
            Optional[Pet]: The reconstructed Pet domain entity if found, None otherwise.
        """
        stmt = select(PetORM).where(PetORM.id == pet_id)
        result = await self.session.execute(stmt)
        orm_pet = result.scalar_one_or_none()

        if not orm_pet:
            return None

        return Pet(
            id=cast(str, orm_pet.id),
            name=cast(str, orm_pet.name),
            species=cast(str, orm_pet.species),
            breed=cast(str, orm_pet.breed) if orm_pet.breed else None
        )

    async def find_by_name_and_species(self, name: str, species: str) -> Optional[Pet]:
        """Finds a pet by its name and species using case-insensitive matching.

        Args:
            name (str): The name of the pet.
            species (str): The species of the pet.

        Returns:
            Optional[Pet]: The reconstructed Pet domain entity if found, None otherwise.
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
            id=cast(str, orm_pet.id),
            name=cast(str, orm_pet.name),
            species=cast(str, orm_pet.species),
            breed=cast(str, orm_pet.breed) if orm_pet.breed else None
        )