import time
from sqlalchemy import (Column, Integer, String,
                        Boolean, BigInteger, ForeignKey,
                        DateTime, Float, UUID, func, ARRAY)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.utils import BaseModel


class ObjConsumerStation(BaseModel):
    name: str
    address: str
    coordinates: str

    __tablename__ = "obj_consumer_stations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_district_id = Column(Integer, ForeignKey('obj_districts.id'), nullable=True)
    obj_area_id = Column(Integer, ForeignKey('obj_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)

    source_station = relationship('ObjSourceStation', uselist=True, lazy='dynamic')
    consumers = relationship('ObjConsumer', uselist=True, lazy='dynamic')


class ObjSourceStation(BaseModel):
    # obj_consumer_station_id: int
    name: str
    address: str
    coordinates: str

    __tablename__ = "obj_source_stations"

    id = Column(Integer, primary_key=True, autoincrement=True)

    obj_consumer_station_id = Column(Integer, ForeignKey('obj_consumer_stations.id'), nullable=True)  # foreign key
    obj_district_id = Column(Integer, ForeignKey('obj_districts.id'), nullable=True)
    obj_area_id = Column(Integer, ForeignKey('obj_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)

    # consumer_stations = relationship('ObjConsumerStation', back_populates='source_stations')
    # consumer_station = relationship('ObjConsumerStation', back_populates="source_station")


class ObjConsumer(BaseModel):
    # obj_consumer_station_id: int
    name: str
    address: str
    coordinates: str
    wall_material: str
    roof_material: str
    total_area: float
    living_area: float
    not_living_area: float
    fact_temp: float
    outside_temp: float
    energy_class: str
    type: str
    operating_mode: str

    __tablename__ = "obj_consumers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_consumer_station_id = Column(Integer, ForeignKey('obj_consumer_stations.id'), nullable=True)

    obj_district_id = Column(Integer, ForeignKey('obj_districts.id'), nullable=True)
    obj_area_id = Column(Integer, ForeignKey('obj_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinates = Column(String, nullable=True, default=False)
    wall_material = Column(String, nullable=True)
    roof_material = Column(String, nullable=True)
    total_area = Column(Float, nullable=True)
    living_area = Column(Float, nullable=True)
    not_living_area = Column(Float, nullable=True)
    fact_temp = Column(Float, nullable=True)
    outside_temp = Column(Float, nullable=True)

    energy_class = Column(String, nullable=True)
    type = Column(String, nullable=True)
    operating_mode = Column(String, nullable=True)

    # consumer_station = relationship('ObjConsumerStation', back_populates="consumers")


class ObjConsumerEvent(BaseModel):
    name: str
    source: str
    system: str
    description: str
    created: None
    closed: None

    __tablename__ = "obj_consumer_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_consumer_id = Column(Integer, ForeignKey('obj_consumers.id'), nullable=True)
    name = Column(String, nullable=True)
    source = Column(String, nullable=True)
    system = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), nullable=True)
    closed = Column(DateTime(timezone=True), nullable=True)


class ObjDistrict(BaseModel):
    name: str
    short_name: str

    __tablename__ = "obj_districts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    short_name = Column(String, nullable=True)

    consumer_station = relationship('ObjConsumerStation', uselist=True, lazy='dynamic')
    source_station = relationship('ObjSourceStation', uselist=True, lazy='dynamic')
    consumers = relationship('ObjConsumer', uselist=True, lazy='dynamic')
    area = relationship('ObjArea', uselist=True, lazy='dynamic')


class ObjArea(BaseModel):
    name: str
    coordinates: str
    fact_temp: float
    last_update_temp: None

    __tablename__ = "obj_areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_district_id = Column(Integer, ForeignKey('obj_districts.id'), nullable=True)
    name = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)
    fact_temp = Column(String, nullable=True)
    last_update_temp = Column(DateTime(timezone=True), nullable=True)

    consumer_station = relationship('ObjConsumerStation', uselist=True, lazy='dynamic')
    source_station = relationship('ObjSourceStation', uselist=True, lazy='dynamic')
    consumers = relationship('ObjConsumer', uselist=True, lazy='dynamic')


class ObjConsumerWeather(BaseModel):
    __tablename__ = "obj_consumer_weathers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_consumer_id = Column(Integer, ForeignKey('obj_consumers.id'), nullable=True)
    temp_dropping = Column(JSONB, nullable=True, default='{}')
    is_actual = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), nullable=True)
