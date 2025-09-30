from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from typing import List


class Base(DeclarativeBase):
    pass


# Association table for many-to-many relationship between beds and plant families
bed_plant_family_association = Table(
    "bed_plant_family",
    Base.metadata,
    Column("bed_id", Integer, ForeignKey("beds.id"), primary_key=True),
    Column(
        "plant_family_id", Integer, ForeignKey("plant_families.id"), primary_key=True
    ),
)


class SQLBed(Base):
    __tablename__ = "beds"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    index: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    # Many-to-many relationship with plant families
    plant_families: Mapped[List["SQLPlantFamily"]] = relationship(
        "SQLPlantFamily", secondary=bed_plant_family_association, back_populates="beds"
    )


class SQLPlantFamily(Base):
    __tablename__ = "plant_families"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    nutrition_requirements: Mapped[str] = mapped_column(Text, nullable=False)
    rotation_time: Mapped[int] = mapped_column(Integer, nullable=False)

    # Many-to-many relationship with beds
    beds: Mapped[List[SQLBed]] = relationship(
        "SQLBed",
        secondary=bed_plant_family_association,
        back_populates="plant_families",
    )
