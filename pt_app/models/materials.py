import time
from sqlalchemy import (Column, Integer, String,
                        Boolean, BigInteger, ForeignKey,
                        DateTime, Float, UUID, func, ARRAY)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy.orm import *
from models.utils import BaseModel, Base

# many to many fields to consumer
material_consumer_walls = Table(
    'material_consumer_walls', Base.metadata,
    Column('material_wall_id', Integer(), ForeignKey('material_walls.id'), primary_key=True),
    Column('obj_consumer_id', Integer(), ForeignKey('obj_consumers.id'), primary_key=True)
)

material_consumer_roofs = Table(
    'material_consumer_roofs', Base.metadata,
    Column('material_roof_id', Integer(), ForeignKey('material_roofs.id'), primary_key=True),
    Column('obj_consumer_id', Integer(), ForeignKey('obj_consumers.id'), primary_key=True)
)


class MaterialWall(BaseModel):
    name: str
    k: float

    __tablename__ = "material_walls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    k = Column(Float, nullable=True)


class MaterialRoof(BaseModel):
    name: str
    k: float

    __tablename__ = "material_roofs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    k = Column(Float, nullable=True)
