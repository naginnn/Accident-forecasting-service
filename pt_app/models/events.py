import time
from sqlalchemy import (Column, Integer, String,
                        Boolean, BigInteger, ForeignKey,
                        DateTime, Float, UUID, func, ARRAY)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.utils import BaseModel


class EventConsumer(BaseModel):
    __tablename__ = 'event_consumers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_consumer_id = Column(Integer, ForeignKey('obj_consumers.id'), nullable=True)
    source = Column(String, nullable=True)
    description = Column(String, nullable=True)
    is_approved = Column(Boolean, nullable=True)
    is_closed = Column(Boolean, nullable=True)
    probability = Column(Float, nullable=True)
    days_of_work = Column(Float, nullable=True)
    created = Column(DateTime(timezone=True), nullable=True)
    closed = Column(DateTime(timezone=True), nullable=True)


class EventType(BaseModel):
    __tablename__ = 'event_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String, nullable=False)


class EventCounter(BaseModel):
    __tablename__ = 'event_counters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_consumer_id = Column(Integer, ForeignKey('obj_consumers.id'), nullable=True)
    event_consumer_id = Column(Integer, ForeignKey('event_consumers.id'), nullable=True)

    contour = Column(String, nullable=True)
    counter_mark = Column(String, nullable=True)
    counter_number = Column(Integer, nullable=True)
    created = Column(DateTime(timezone=True), nullable=True)
    gcal_in_system = Column(Float, nullable=True)
    gcal_out_system = Column(Float, nullable=True)
    subset = Column(Float, nullable=True)
    leak = Column(Float, nullable=True)
    supply_temp = Column(Float, nullable=True)
    return_temp = Column(Float, nullable=True)
    work_hours_counter = Column(Float, nullable=True)
    heat_thermal_energy = Column(Float, nullable=True)
    errors = Column(String, nullable=True)
    errors_desc = Column(String, nullable=True)
