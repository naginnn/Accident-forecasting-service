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
    system = Column(String, nullable=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), nullable=True)
    closed = Column(DateTime(timezone=True), nullable=True)
