import time

import pandas as pd
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker, Session
from models.objects import ObjDistrict, ObjArea, ObjConsumerStation, ObjSourceStation, ObjConsumer
from pkg.ya_api import get_one_coordinate, get_coordinates


def get_district(db_session: Session, data: dict):
    district = db_session.execute(select(ObjDistrict).filter(ObjDistrict.name == data.get('district'))).scalar()
    if district is None:
        district = ObjDistrict(name=data.get('district'))
    return district


def get_area(db_session: Session, data: dict):
    area = db_session.execute(select(ObjArea).filter(ObjArea.name == data.get('area'))).scalar()
    if area is None:
        pos = get_one_coordinate(data.get('area'))
        area = ObjArea(name=data.get('area'), coordinates=pos, fact_temp=0.0)
    return area


def to_db(db_session: Session):
    df = pd.read_excel('test.xlsx', sheet_name='full')
    start_time = time.time()
    for index, row in df.iterrows():
        obj_consumer_station = db_session.execute(select(ObjConsumerStation)
                                                  .filter(ObjConsumerStation.name == row['Nº ЦТП (ИТП)'])).scalar()
        if not obj_consumer_station:
            data = get_coordinates(adr=row['Адрес ЦТП (ИТП)'])
            obj_district = get_district(db_session, data=data)
            obj_area = get_area(db_session, data=data)
            obj_consumer_station = ObjConsumerStation(
                name=row['Nº ЦТП (ИТП)'],
                address=row['Адрес ЦТП (ИТП)'],
                coordinates=data.get('pos')
            )
            db_session.add(obj_district)
            db_session.add(obj_area)
            db_session.flush()

            obj_area.obj_district_id = obj_district.id
            obj_consumer_station.obj_district_id = obj_district.id
            obj_consumer_station.obj_area_id = obj_area.id

            # db_session.add(obj_consumer_station)

        obj_source_station = db_session.execute(select(ObjSourceStation)
                                                .filter(ObjSourceStation.name == row['Источник'])).scalar()
        if not obj_source_station:
            data = get_coordinates(adr=row['Адрес источника'])
            obj_district = get_district(db_session, data=data)
            obj_area = get_area(db_session, data=data)
            obj_source_station = ObjSourceStation(
                name=row['Источник'],
                address=row['Адрес источника'],
                coordinates=data.get('pos')
            )

            db_session.add(obj_district)
            db_session.add(obj_area)
            db_session.flush()
            obj_area.obj_district_id = obj_district.id
            obj_source_station.obj_district_id = obj_district.id
            obj_source_station.obj_area_id = obj_area.id

        obj_consumer = db_session.execute(select(ObjConsumer)
                                          .filter(ObjConsumer.address == row['Адрес потребителя'])).scalar()
        if not obj_consumer:
            data = get_coordinates(adr=row['Адрес потребителя'])
            obj_district = get_district(db_session, data=data)
            obj_area = get_area(db_session, data=data)
            obj_consumer = ObjConsumer(
                name=row['Назначение здания потребителя'],
                address=row['Адрес потребителя'],
                coordinates=data.get('pos'),
                wall_material=row['Материал стен'],
                roof_material=row['Материал кровли'],
                total_area=row['Площадь'],
                living_area=row['Жилая площадь'],
                not_living_area=row['Не жилая площадь'],
                fact_temp=0.0,
                outside_temp=0.0,
                energy_class=row['Класс энерг. Эфф.'],
                type=row['Тип объекта'],
                operating_mode=row['Время работы'],
            )
            db_session.add(obj_district)
            db_session.add(obj_area)
            db_session.flush()

            obj_area.obj_district_id = obj_district.id
            obj_consumer.obj_district_id = obj_district.id
            obj_consumer.obj_area_id = obj_area.id

        obj_consumer_station.source_station.append(obj_source_station)
        obj_consumer_station.consumers.append(obj_consumer)

        db_session.add(obj_consumer_station)
        db_session.commit()
        # break
    print(time.time() - start_time)
    print('Success')