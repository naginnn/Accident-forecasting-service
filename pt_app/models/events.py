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