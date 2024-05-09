import time
from sqlalchemy import (Column, Integer, String,
                        Boolean, BigInteger, ForeignKey,
                        DateTime, Float, UUID, func, ARRAY)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.utils import BaseModel


class PredictionAccident(BaseModel):
    __tablename__ = 'prediction_accidents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_consumer_station_id = Column(Integer, ForeignKey('obj_consumer_stations.id'), nullable=True)
    obj_consumer_id = Column(Integer, ForeignKey('obj_consumers.id'), nullable=True)
    is_accident = Column(Boolean, nullable=True)
    percent = Column(Float, nullable=True)
    is_approved = Column(Boolean, nullable=True)
    is_actual = Column(Boolean, nullable=True)
    created = Column(DateTime(timezone=True), nullable=True)
    closed = Column(DateTime(timezone=True), nullable=True)
