from sqlalchemy import *
from sqlalchemy.orm import *
from models.utils import BaseModel, Base


class LocationDistrict(BaseModel):
    __tablename__ = "location_districts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    short_name = Column(String, nullable=True)

    ### поправить
    consumer_station = relationship('ObjConsumerStation', uselist=True, lazy='dynamic')
    source_station = relationship('ObjSourceStation', uselist=True, lazy='dynamic')
    consumers = relationship('ObjConsumer', uselist=True, lazy='dynamic')
    areas = relationship('LocationArea', uselist=True, lazy='dynamic')
    UniqueConstraint(name, name='uni_location_districts_name')


class LocationArea(BaseModel):
    __tablename__ = "location_areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_district_id = Column(Integer, ForeignKey('location_districts.id'), nullable=True)
    name = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)
    weathers = relationship('WeatherArea', uselist=True, lazy='dynamic')
    UniqueConstraint(name, name='uni_location_areas_name')
