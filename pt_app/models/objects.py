from sqlalchemy import *
from sqlalchemy.orm import *
from models.utils import BaseModel, Base
from sqlalchemy.dialects.postgresql import JSONB

obj_source_consumer_stations = Table(
    'obj_source_consumer_stations', Base.metadata,
    Column('obj_source_station_id', Integer(), ForeignKey('obj_source_stations.id'), primary_key=True),
    Column('obj_consumer_station_id', Integer(), ForeignKey('obj_consumer_stations.id'), primary_key=True)
)


class ObjConsumerStation(BaseModel):
    name: str
    address: str

    __tablename__ = "obj_consumer_stations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_district_id = Column(Integer, ForeignKey('location_districts.id'), nullable=True)
    location_area_id = Column(Integer, ForeignKey('location_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    geo_data = Column(JSONB, nullable=True, default='{}')
    type = Column(String, nullable=True)
    place_type = Column(String, nullable=True)
    ods_name = Column(String, nullable=True)
    ods_address = Column(String, nullable=True)
    ods_id_uu = Column(String, nullable=True)
    ods_manager_company = Column(String, nullable=True)

    source_stations = relationship('ObjSourceStation', uselist=True, secondary='obj_source_consumer_stations',
                                   lazy='dynamic')
    consumers = relationship('ObjConsumer', uselist=True, lazy='dynamic')

    UniqueConstraint(name, name='uni_obj_consumer_stations_name')
    # UniqueConstraint(address, name='uni_obj_consumer_stations_address')


class ObjSourceStation(BaseModel):
    name: str
    address: str

    __tablename__ = "obj_source_stations"

    id = Column(Integer, primary_key=True, autoincrement=True)

    location_district_id = Column(Integer, ForeignKey('location_districts.id'), nullable=True)
    location_area_id = Column(Integer, ForeignKey('location_areas.id'), nullable=True)

    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    geo_data = Column(JSONB, nullable=True, default='{}')

    e_power = Column(String, nullable=True)
    t_power = Column(BigInteger, nullable=True)
    boiler_count = Column(BigInteger, nullable=True)
    turbine_count = Column(BigInteger, nullable=True)
    launched_date = Column(DateTime(timezone=True), nullable=True)

    consumer_stations = relationship('ObjConsumerStation', uselist=True, secondary='obj_source_consumer_stations',
                                     lazy='dynamic')

    UniqueConstraint(name, name='uni_obj_source_stations_name')


class ObjConsumer(BaseModel):
    __tablename__ = "obj_consumers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_consumer_station_id = Column(Integer, ForeignKey('obj_consumer_stations.id'), nullable=True)
    location_district_id = Column(Integer, ForeignKey('location_districts.id'), nullable=True)
    location_area_id = Column(Integer, ForeignKey('location_areas.id'), nullable=True)

    address = Column(String, nullable=True)
    geo_data = Column(JSONB, nullable=True, default='{}')

    street = Column(String, nullable=True)
    house_type = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    corpus_number = Column(String, nullable=True)
    soor_type = Column(String, nullable=True)
    soor_number = Column(String, nullable=True)

    balance_holder = Column(String, nullable=True)
    load_gvs = Column(String, nullable=True)
    load_fact = Column(String, nullable=True)
    heat_load = Column(String, nullable=True)
    vent_load = Column(String, nullable=True)

    total_area = Column(Float, nullable=True)
    target = Column(String, nullable=True)
    b_class = Column(String, nullable=True)
    floors = Column(String, nullable=True)
    number = Column(String, nullable=True)
    wear_pct = Column(String, nullable=True)
    build_year = Column(String, nullable=True)
    type = Column(String, nullable=True)
    sock_type = Column(String, nullable=True)
    energy_class = Column(String, nullable=True)
    operating_mode = Column(String, nullable=True)
    priority = Column(Integer, nullable=True)
    is_dispatch = Column(Boolean, nullable=True)

    temp_conditions = Column(JSONB, nullable=True, default='{}')
    events = relationship('EventConsumer', uselist=True, lazy='dynamic')
    weather_fall = relationship('WeatherConsumerFall', uselist=True, lazy='dynamic')
    wall_material = relationship('MaterialWall', uselist=True, secondary='material_consumer_walls',
                                 lazy='dynamic')

    UniqueConstraint(address, name='uni_obj_consumers_address')
