import sys
import time

import pandas as pd
from sqlalchemy import create_engine, text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import insert as ins
from models.locations import *
from models.accidents import *
from models.events import *
from models.objects import *
from models.materials import *
from models.weathers import *
from pkg.utils import FakeJob


class SaveView:
    @staticmethod
    def save_locations(session: Session, df: pd.DataFrame):
        location_districts = list(set(
            df['okrug_potrebitelja'].unique().tolist()
            + df['okrug_tstp_itp'].unique().tolist()
        ))
        # location_areas
        districts = {}
        for district in location_districts:
            location_district = ins(LocationDistrict).values(
                name=district,
            )
            do_upd_upd = location_district.on_conflict_do_update(
                constraint='uni_location_districts_name',
                set_={'name': district}
            ).returning(LocationDistrict.id)
            districts[district] = session.execute(do_upd_upd).scalar()

        areas = {}
        loc_area_consumer = df['rajon_potrebitelja'].unique().tolist()
        loc_area_source = df['rajon_tstp_itp'].unique().tolist()
        for area_cons, area_source in zip(loc_area_consumer, loc_area_source):
            loc_area = df[(df['rajon_potrebitelja'] == area_cons)]
            location_area = ins(LocationArea).values(
                name=area_cons,
            )
            do_upd_upd = location_area.on_conflict_do_update(
                constraint='uni_location_areas_name',
                set_={'name': area_cons,
                      'coordinates': loc_area['koordinaty_potrebitelja'].iloc[0,],
                      'location_district_id': districts.get(loc_area['okrug_potrebitelja'].iloc[0,]),
                      }
            ).returning(LocationArea.id)
            areas[area_cons] = session.execute(do_upd_upd).scalar()

            loc_area = df[(df['rajon_tstp_itp'] == area_source)]
            location_area = ins(LocationArea).values(
                name=area_source,
            )
            do_upd_upd = location_area.on_conflict_do_update(
                constraint='uni_location_areas_name',
                set_={'name': area_source,
                      'coordinates': loc_area['koordinaty_tstp_itp'].iloc[0,],
                      'location_district_id': districts.get(loc_area['okrug_tstp_itp'].iloc[0,]),
                      }
            ).returning(LocationArea.id)
            areas[area_cons] = session.execute(do_upd_upd).scalar()
        session.commit()
        return dict(districts=districts, areas=areas)

    @staticmethod
    def save_objects(session: Session, df: pd.DataFrame, locations: dict, all_events: pd.DataFrame):
        districts, areas = locations.get('districts'), locations.get('areas')
        for index, row in df.iterrows():
            obj_consumer_station = ins(ObjConsumerStation).values(
                name=row['n_tstp_itp'],
                address=row['adres_tstp_itp'],
                location_district_id=districts.get(row['okrug_tstp_itp']),
                location_area_id=areas.get(row['rajon_tstp_itp']),
                coordinates=row['koordinaty_tstp_itp'],

            )

            do_upd_upd = obj_consumer_station.on_conflict_do_update(
                constraint='uni_obj_consumer_stations_name',
                set_={
                    "address": row['adres_tstp_itp'],
                    "coordinates": row['koordinaty_tstp_itp'],
                    "location_district_id": districts.get(row['okrug_tstp_itp']),
                    "location_area_id": areas.get(row['rajon_tstp_itp']),
                }
            ).returning(ObjConsumerStation)
            obj_consumer_station = session.execute(do_upd_upd).scalar()

            obj_source_station = ins(ObjSourceStation).values(
                name=row['istochnik'],
                address=row['adres_istochnika'],
                location_district_id=districts.get(row['okrug_tstp_itp']),
                location_area_id=areas.get(row['rajon_tstp_itp']),
                coordinates=row['koordinaty_istochnika'],

            )

            do_upd_upd = obj_source_station.on_conflict_do_update(
                constraint='uni_obj_source_stations_name',
                set_={
                    "address": row['adres_istochnika'],
                    "coordinates": row['koordinaty_istochnika'],
                    "location_district_id": districts.get(row['okrug_tstp_itp']),
                    "location_area_id": areas.get(row['rajon_tstp_itp']),
                }
            ).returning(ObjSourceStation)

            obj_source_station = session.execute(do_upd_upd).scalar()
            try:
                obj_source_station.consumer_stations.append(obj_consumer_station)
                session.commit()
            except Exception as e:
                session.rollback()

            obj_consumer = ins(ObjConsumer).values(
                name=row['naznachenie_zdanija_potrebitelja'],
                address=row['adres_potrebitelja'],
                coordinates=row['koordinaty_potrebitelja'],
                # wall_material=row['material_sten'],
                # roof_material=row['material_krovli'],
                total_area=row['ploschad'],
                living_area=row['zhilaja_ploschad'],
                not_living_area=row['ne_zhilaja_ploschad'],
                energy_class=row['klass_energ_eff'],
                type=row['tip_obekta'],
                operating_mode=row['vremja_raboty'],
                priority=row['priority'],
                temp_conditions=row['temp_conditions'],
                obj_consumer_station_id=obj_consumer_station.id,
                location_district_id=districts.get(row['okrug_potrebitelja']),
                location_area_id=areas.get(row['rajon_potrebitelja']),
            )

            do_upd_upd = obj_consumer.on_conflict_do_update(
                constraint='uni_obj_consumers_address',
                set_=dict(name=row['naznachenie_zdanija_potrebitelja'],
                          coordinates=row['koordinaty_potrebitelja'],
                          # wall_material=row['material_sten'],
                          # roof_material=row['material_krovli'],
                          total_area=row['ploschad'],
                          living_area=row['zhilaja_ploschad'],
                          not_living_area=row['ne_zhilaja_ploschad'],
                          energy_class=row['klass_energ_eff'],
                          type=row['tip_obekta'],
                          operating_mode=row['vremja_raboty'],
                          priority=row['priority'],
                          temp_conditions=row['temp_conditions'],
                          obj_consumer_station_id=obj_consumer_station.id,
                          location_district_id=districts.get(row['okrug_potrebitelja']),
                          location_area_id=areas.get(row['rajon_potrebitelja']), )
            ).returning(ObjConsumer)
            # obj_consumer = session.execute(do_upd_upd).scalar()
            obj_consumer = session.execute(do_upd_upd).scalar()
            events = all_events[all_events['unom'] == row['unom']]
            for index, row in events.iterrows():
                event_consumer = EventConsumer()
                event_consumer.obj_consumer_id = obj_consumer.id
                event_consumer.source = row['source']
                event_consumer.description = row['work_name']
                event_consumer.is_approved = True
                event_consumer.is_closed = True
                event_consumer.probability = 100.0
                event_consumer.days_of_work = row['days_of_work']
                event_consumer.created = row['create_date']
                event_consumer.closed = row['close_date']
                session.add(event_consumer)
            session.commit()


# сохранить без подгрузки координат
def save_for_view(session: Session, tables: dict):
    job = FakeJob.get_current_job()
    df = tables.get("full")
    events = tables.get("events_all")
    locations = SaveView.save_locations(session=session, df=df)
    SaveView.save_objects(session=session, df=df, locations=locations, all_events=events)
    print('Success')


def save_for_predict(session: Session, tables: dict):
    pass


def save_predicated(session: Session, df: pd.DataFrame):
    pass


def update_coordinates(session: Session):
    pass

# if __name__ == '__main__':
#     print()
#     df = pd.read_excel('test.xlsx', sheet_name='full')
#     save_for_view(df=df)
