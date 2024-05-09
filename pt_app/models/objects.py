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
    obj_district_id = Column(Integer, ForeignKey('obj_districts.id'), nullable=True)
    obj_area_id = Column(Integer, ForeignKey('obj_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)

    source_stations = relationship('ObjSourceStation', uselist=True, secondary='obj_source_consumer_stations',
                                   lazy='dynamic', backref='consumer_stations')
    consumers = relationship('ObjConsumer', uselist=True, lazy='dynamic')
    accidents = relationship('PredictionAccident', uselist=True, lazy='dynamic')


class ObjSourceStation(BaseModel):
    # obj_consumer_station_id: int
    name: str
    address: str
    coordinates: str

    __tablename__ = "obj_source_stations"

    id = Column(Integer, primary_key=True, autoincrement=True)

    obj_district_id = Column(Integer, ForeignKey('obj_districts.id'), nullable=True)
    obj_area_id = Column(Integer, ForeignKey('obj_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)

    consumer_stations = relationship('ObjConsumerStation', uselist=True, secondary='obj_source_consumer_stations',
                                     lazy='dynamic', backref='source_stations')


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
    wall_material = relationship('MaterialWall', uselist=True, secondary='material_consumer_wall',
                                 lazy='dynamic')
    roof_material = relationship('MaterialRoof', uselist=True, secondary='material_consumer_roof',
                                 lazy='dynamic')
