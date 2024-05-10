from sqlalchemy import *
from sqlalchemy.orm import *
from models.utils import BaseModel, Base

obj_source_consumer_stations = Table(
    'obj_source_consumer_stations', Base.metadata,
    Column('obj_source_station_id', Integer(), ForeignKey('obj_source_stations.id'), primary_key=True),
    Column('obj_consumer_station_id', Integer(), ForeignKey('obj_consumer_stations.id'), primary_key=True)
)


class ObjConsumerStation(BaseModel):
    name: str
    address: str
    coordinates: str

    __tablename__ = "obj_consumer_stations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_district_id = Column(Integer, ForeignKey('location_districts.id'), nullable=True)
    location_area_id = Column(Integer, ForeignKey('location_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)

    source_stations = relationship('ObjSourceStation', uselist=True, secondary='obj_source_consumer_stations',
                                   lazy='dynamic')
    consumers = relationship('ObjConsumer', uselist=True, lazy='dynamic')
    accidents = relationship('PredictionAccident', uselist=True, lazy='dynamic')

    UniqueConstraint(name, name='uni_obj_consumer_stations_name')
    # UniqueConstraint(address, name='uni_obj_consumer_stations_address')


class ObjSourceStation(BaseModel):
    name: str
    address: str
    coordinates: str

    __tablename__ = "obj_source_stations"

    id = Column(Integer, primary_key=True, autoincrement=True)

    location_district_id = Column(Integer, ForeignKey('location_districts.id'), nullable=True)
    location_area_id = Column(Integer, ForeignKey('location_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)

    consumer_stations = relationship('ObjConsumerStation', uselist=True, secondary='obj_source_consumer_stations',
                                     lazy='dynamic')

    UniqueConstraint(name, name='uni_obj_source_stations_name')


class ObjConsumer(BaseModel):
    __tablename__ = "obj_consumers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_consumer_station_id = Column(Integer, ForeignKey('obj_consumer_stations.id'), nullable=True)
    location_district_id = Column(Integer, ForeignKey('location_districts.id'), nullable=True)
    location_area_id = Column(Integer, ForeignKey('location_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinates = Column(String, nullable=True, default=False)
    total_area = Column(Float, nullable=True)
    living_area = Column(Float, nullable=True)
    not_living_area = Column(Float, nullable=True)

    type = Column(String, nullable=True)
    energy_class = Column(String, nullable=True)
    operating_mode = Column(String, nullable=True)
    priority = Column(Integer, nullable=True)

    accidents = relationship('PredictionAccident', uselist=True, lazy='dynamic')
    events = relationship('EventConsumer', uselist=True, lazy='dynamic')
    weather_fall = relationship('WeatherConsumerFall', uselist=True, lazy='dynamic')
    wall_material = relationship('MaterialWall', uselist=True, secondary='material_consumer_walls',
                                 lazy='dynamic')
    roof_material = relationship('MaterialRoof', uselist=True, secondary='material_consumer_roofs',
                                 lazy='dynamic')

    UniqueConstraint(address, name='uni_obj_consumers_address')
