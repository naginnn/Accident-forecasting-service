import time
from sqlalchemy import (Column, Integer, String,
                        Boolean, BigInteger, ForeignKey,
                        DateTime, Float, UUID, func, ARRAY)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.utils import BaseModel


class WeatherArea(BaseModel):
    __tablename__ = "weather_areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_area_id = Column(Integer, ForeignKey('location_areas.id'), nullable=True)
    temp_info = Column(JSONB, nullable=True, default='{}')
    created = Column(DateTime(timezone=True), nullable=True)


class WeatherConsumerFall(BaseModel):
    __tablename__ = "weather_consumer_falls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_consumer_id = Column(Integer, ForeignKey('obj_consumers.id'), nullable=True)
    temp_dropping = Column(JSONB, nullable=True, default='{}')
    created = Column(DateTime(timezone=True), nullable=True)
