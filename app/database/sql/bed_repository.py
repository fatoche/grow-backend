from typing import List, Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload

from app.database.base.bed import BedRepository
from app.models.bed import Bed, BedCreate
from app.database.sql.models import SQLBed


class SQLBedRepository(BedRepository):
    """PostgreSQL implementation of BedRepository using SQLAlchemy"""

    def __init__(self, database_url: str):
        self.database_url = database_url.replace(
            "postgresql://", "postgresql+asyncpg://"
        )
        self.engine = create_async_engine(self.database_url, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    def _sql_bed_to_bed(self, sql_bed: SQLBed) -> Bed:
        """Convert SQLBed model to Bed Pydantic model"""
        return Bed(
            id=sql_bed.id,
            index=sql_bed.index,
            length=sql_bed.length,
            width=sql_bed.width,
            plant_families=[pf.id for pf in sql_bed.plant_families],
        )

    async def create_bed(self, bed: BedCreate) -> Bed:
        """Create a single bed in PostgreSQL"""
        async with self.async_session() as session:
            # Get the next available index
            max_index_result = await session.execute(select(func.max(SQLBed.index)))
            max_index = max_index_result.scalar() or 0
            index = max_index + 1

            sql_bed = SQLBed(length=bed.length, width=bed.width, index=index)
            # Initialize relationship to avoid lazy loading in _sql_bed_to_bed which is
            # outside the async context and would raise a missing greenlet error
            sql_bed.plant_families = []

            session.add(sql_bed)
            await session.commit()

            return self._sql_bed_to_bed(sql_bed)

    async def create_multiple_beds(self, beds: List[BedCreate]) -> List[Bed]:
        """Create multiple beds in PostgreSQL"""
        async with self.async_session() as session:
            # Since this is called after delete_all_beds, we start from index 1
            sql_beds = []
            for i, bed in enumerate(beds):
                index = i + 1
                sql_bed = SQLBed(length=bed.length, width=bed.width, index=index)
                # Initialize relationship to avoid lazy loading in _sql_bed_to_bed which
                # is outside the async context and would raise a missing greenlet error.
                sql_bed.plant_families = []  
                sql_beds.append(sql_bed)
                session.add(sql_bed)

            await session.commit()

            return [self._sql_bed_to_bed(sql_bed) for sql_bed in sql_beds]

    async def get_bed_by_id(self, bed_id: int) -> Optional[Bed]:
        """Get a bed by its ID from PostgreSQL"""
        async with self.async_session() as session:
            result = await session.execute(
                select(SQLBed)
                .options(selectinload(SQLBed.plant_families))
                .where(SQLBed.id == bed_id)
            )
            sql_bed = result.scalar_one_or_none()
            if sql_bed:
                return self._sql_bed_to_bed(sql_bed)
            return None

    async def get_all_beds(self) -> List[Bed]:
        """Get all beds from PostgreSQL"""
        async with self.async_session() as session:
            result = await session.execute(
                select(SQLBed)
                .options(selectinload(SQLBed.plant_families))
                .order_by(SQLBed.index)
            )
            sql_beds = result.scalars().all()
            return [self._sql_bed_to_bed(sql_bed) for sql_bed in sql_beds]

    async def update_bed(self, bed_id: int, bed: BedCreate) -> Optional[Bed]:
        """Update a bed in PostgreSQL"""
        async with self.async_session() as session:
            result = await session.execute(
                select(SQLBed)
                .options(selectinload(SQLBed.plant_families))
                .where(SQLBed.id == bed_id)
            )
            sql_bed = result.scalar_one_or_none()

            if sql_bed:
                sql_bed.length = bed.length
                sql_bed.width = bed.width
                await session.commit()
                return self._sql_bed_to_bed(sql_bed)

            return None

    async def delete_bed(self, bed_id: int) -> bool:
        """Delete a bed from PostgreSQL"""
        async with self.async_session() as session:
            result = await session.execute(delete(SQLBed).where(SQLBed.id == bed_id))
            await session.commit()
            return result.rowcount > 0

    async def delete_all_beds(self) -> int:
        """Delete all beds from PostgreSQL"""
        async with self.async_session() as session:
            result = await session.execute(delete(SQLBed))
            await session.commit()
            return result.rowcount

    async def close(self):
        """Close the database connection"""
        await self.engine.dispose()
