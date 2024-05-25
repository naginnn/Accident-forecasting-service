import time
from sqlalchemy import (Column, Integer, String,
                        Boolean, BigInteger, ForeignKey,
                        DateTime, Float, UUID, func, ARRAY)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy.orm import *
from models.utils import BaseModel, Base


class ModelInfo(BaseModel):
    name: str
    path: str
    metrics: str
    accuracy: float
    feature_importance: dict
    created: DateTime

    __tablename__ = "model_infos"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=True)
    path = Column(String, nullable=True)
    metrics = Column(String, nullable=True)
    accuracy = Column(Float, nullable=True, default=False)
    feature_importance = Column(JSONB, nullable=True, default='{}')
    created = Column(DateTime(timezone=True), nullable=True)
