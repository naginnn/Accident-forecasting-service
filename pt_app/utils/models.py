import uuid
from datetime import timedelta, datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.collections import InstrumentedList

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def to_dict(self, rel=True, ignored_fields=(), **additional_fields):
        attrs = {} or additional_fields
        for attribute, value in self.__dict__.items():
            if attribute in ignored_fields:
                continue
            if not attribute.startswith('_'):
                if isinstance(value, InstrumentedList):
                    if rel:
                        attrs[attribute] = []
                        for val in value:
                            attrs[attribute].append(val.to_dict(rel, ignored_fields))
                        continue
                    else:
                        continue
                if isinstance(value, uuid.UUID):
                    attrs[attribute] = str(value)
                elif isinstance(value, datetime):
                    val = value + timedelta(hours=3)
                    attrs[attribute] = val.strftime("%Y/%m/%d, %H:%M")
                else:
                    attrs[attribute] = value
        return attrs


def get_dict(obj, ignored_fields=None, date_format=None, compress_list=None):
    if not isinstance(obj, list):
        obj = [obj]
    fields = []
    for o in obj:
        if isinstance(o[0], BaseModel):
            fields.append(o[0].to_dict(ignored_fields=ignored_fields if ignored_fields else ()))
        else:
            new_obj = {}
            for name, value in o._mapping.items():
                if compress_list:
                    if isinstance(value, list):
                        new_obj[name] = ','.join(value)
                        continue
                if isinstance(value, uuid.UUID):
                    new_obj[name] = str(value)
                elif isinstance(value, datetime):
                    val = value + timedelta(hours=3)
                    new_obj[name] = val.strftime(date_format if date_format else "%Y/%m/%d, %H:%M")
                elif value is None:
                    new_obj[name] = 'Нет данных'
                else:
                    new_obj[name] = value
            fields.append(new_obj)
    return fields
