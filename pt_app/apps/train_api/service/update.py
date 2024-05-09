import time

import pandas as pd
from sqlalchemy import create_engine, text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
from models.objects import ObjDistrict, ObjArea, ObjConsumerStation, ObjSourceStation, ObjConsumer, ObjConsumerWeather
from pkg.utils import FakeJob
from pkg.ya_api import get_one_coordinate, get_coordinates, get_weather


def get_district(session: Session, data: dict):
    district = session.execute(select(ObjDistrict).filter(ObjDistrict.name == data.get('district'))).scalar()
    if district is None:
        district = ObjDistrict(name=data.get('district'))
    return district


def get_area(session: Session, data: dict):
    area = session.execute(select(ObjArea).filter(ObjArea.name == data.get('area'))).scalar()
    if area is None:
        pos = get_one_coordinate(data.get('area'))
        temp_data = get_weather(pos.split(' ')[0], pos.split(' ')[1])
        area = ObjArea(name=data.get('area'), coordinates=pos, temp_data=temp_data)
    return area


# передать плоскую таблицу
def save_for_view(session: Session, df: pd.DataFrame):
    job = FakeJob.get_current_job()
    start_time = time.time()
    for index, row in df.iterrows():
        obj_consumer_station = session.execute(select(ObjConsumerStation)
                                               .filter(ObjConsumerStation.name == row['Nº ЦТП (ИТП)'])).scalar()
        if not obj_consumer_station:
            data = get_coordinates(adr=row['Адрес ЦТП (ИТП)'])
            obj_district = get_district(session, data=data)
            obj_area = get_area(session, data=data)
            obj_consumer_station = ObjConsumerStation(
                name=row['Nº ЦТП (ИТП)'],
                address=row['Адрес ЦТП (ИТП)'],
                coordinates=data.get('pos')
            )
            session.add(obj_district)
            session.add(obj_area)
            session.flush()

            obj_area.obj_district_id = obj_district.id
            obj_consumer_station.obj_district_id = obj_district.id
            obj_consumer_station.obj_area_id = obj_area.id

            # db_session.add(obj_consumer_station)

        obj_source_station = session.execute(select(ObjSourceStation)
                                             .filter(ObjSourceStation.name == row['Источник'])).scalar()
        if not obj_source_station:
            data = get_coordinates(adr=row['Адрес источника'])
            obj_district = get_district(session, data=data)
            obj_area = get_area(session, data=data)
            obj_source_station = ObjSourceStation(
                name=row['Источник'],
                address=row['Адрес источника'],
                coordinates=data.get('pos')
            )

            session.add(obj_district)
            session.add(obj_area)
            session.flush()
            obj_area.obj_district_id = obj_district.id
            obj_source_station.obj_district_id = obj_district.id
            obj_source_station.obj_area_id = obj_area.id

        obj_consumer = session.execute(select(ObjConsumer)
                                       .filter(ObjConsumer.address == row['Адрес потребителя'])).scalar()
        if not obj_consumer:
            data = get_coordinates(adr=row['Адрес потребителя'])
            obj_district = get_district(session, data=data)
            obj_area = get_area(session, data=data)
            obj_consumer = ObjConsumer(
                name=row['Назначение здания потребителя'],
                address=row['Адрес потребителя'],
                coordinates=data.get('pos'),
                wall_material=row['Материал стен'],
                roof_material=row['Материал кровли'],
                total_area=row['Площадь'],
                living_area=row['Жилая площадь'],
                not_living_area=row['Не жилая площадь'],
                energy_class=row['Класс энерг. Эфф.'],
                type=row['Тип объекта'],
                operating_mode=row['Время работы'],
            )
            session.add(obj_district)
            session.add(obj_area)
            session.flush()

            obj_area.obj_district_id = obj_district.id
            obj_consumer.obj_district_id = obj_district.id
            obj_consumer.obj_area_id = obj_area.id

        obj_consumer_station.source_station.append(obj_source_station)
        obj_consumer_station.consumers.append(obj_consumer)

        session.add(obj_consumer_station)
        session.commit()
        # break
    print(time.time() - start_time)
    print('Success')


def save_for_predict(session: Session, df: pd.DataFrame):
    pass


def save_predicated(session: Session, df: pd.DataFrame):
    pass


def update_coordinates(session: Session):
    pass


if __name__ == '__main__':
    print()
    df = pd.read_excel('test.xlsx', sheet_name='full')
    save_for_view(df=df)
