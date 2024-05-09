import time
from sqlalchemy import (Column, Integer, String,
                        Boolean, BigInteger, ForeignKey,
                        DateTime, Float, UUID, func, ARRAY)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.utils import BaseModel

# type LocationDistrict struct {
# 	Areas     []LocationArea `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"consumers"`
# }


class LocationDistrict(BaseModel):
    name: str
    short_name: str

    __tablename__ = "location_districts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    short_name = Column(String, nullable=True)


    ### поправить
    # consumer_station = relationship('ObjConsumerStation', uselist=True, lazy='dynamic')
    # source_station = relationship('ObjSourceStation', uselist=True, lazy='dynamic')
    # consumers = relationship('ObjConsumer', uselist=True, lazy='dynamic')
    areas = relationship('LocationArea', uselist=True, lazy='dynamic')


class LocationArea(BaseModel):
    name: str
    coordinates: str
    temp_data: dict
    last_update_temp: None

    __tablename__ = "location_areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_district_id = Column(Integer, ForeignKey('obj_districts.id'), nullable=True)
    name = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)
    weathers = relationship('WeatherArea', uselist=True, lazy='dynamic')