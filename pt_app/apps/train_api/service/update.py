import datetime
import sys
import time
import os
from catboost import CatBoostClassifier
import pandas as pd
from sqlalchemy import create_engine, text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import insert as ins
from models.locations import *
from models.events import *
from models.ml_info import ModelInfo
from models.objects import *
from models.materials import *
from models.utils import create_or_update
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

            material_wall = ins(MaterialWall).values(
                name=row['wall_material_description'],
                k=row['coef'],
            )

            do_upd_upd = material_wall.on_conflict_do_update(
                constraint='uni_material_walls_name',
                set_={
                    "k": row['coef'],
                }
            ).returning(MaterialWall)

            material_wall = session.execute(do_upd_upd).scalar()

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
            try:
                obj_consumer.wall_material.append(material_wall)
                session.commit()
            except Exception as e:
                session.rollback()

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

    @staticmethod
    def save_objects_new(session: Session, df: pd.DataFrame, events: pd.DataFrame, counter_events: pd.DataFrame):
        for index, row in df.iterrows():
            location_district = create_or_update(
                session=session,
                Model=LocationDistrict,
                constraint="uni_location_districts_name",
                create_fields=dict(
                    name=row['obj_consumer_station_location_district'],
                ),
                update_fields=dict(
                    name=row['obj_consumer_station_location_district'],
                )
            )

            location_area = create_or_update(
                session=session,
                Model=LocationArea,
                constraint="uni_location_areas_name",
                create_fields=dict(
                    name=row['obj_consumer_station_location_area'],
                    location_district_id=location_district.id,
                ),
                update_fields=dict(
                    name=row['obj_consumer_station_location_area'],
                    location_district_id=location_district.id,
                )
            )

            obj_consumer_station = create_or_update(
                session=session,
                Model=ObjConsumerStation,
                constraint="uni_obj_consumer_stations_name",
                create_fields=dict(
                    location_district_id=location_district.id,
                    location_area_id=location_area.id,
                    name=row['obj_consumer_station_name'],
                    address=row['obj_consumer_station_address'],
                    type=row['obj_consumer_station_type'],
                    place_type=row['obj_consumer_station_place_type'],
                    ods_name=row['obj_consumer_station_ods_name'],
                    ods_address=row['obj_consumer_station_ods_address'],
                    ods_id_uu=row['obj_consumer_station_ods_id_yy'],
                    ods_manager_company=row['obj_consumer_station_ods_manager_company'],
                    geo_data=row["obj_consumer_station_coordinates"],
                ),
                update_fields=dict(
                    address=row['obj_consumer_station_address'],
                    type=row['obj_consumer_station_type'],
                    place_type=row['obj_consumer_station_place_type'],
                    ods_name=row['obj_consumer_station_ods_name'],
                    ods_address=row['obj_consumer_station_ods_address'],
                    ods_id_uu=row['obj_consumer_station_ods_id_yy'],
                    ods_manager_company=row['obj_consumer_station_ods_manager_company'],
                    geo_data=row["obj_consumer_station_coordinates"],
                )
            )

            obj_source_station = create_or_update(
                session=session,
                Model=ObjSourceStation,
                constraint="uni_obj_source_stations_name",
                create_fields=dict(
                    location_district_id=location_district.id,
                    location_area_id=location_area.id,
                    name=row["obj_source_name"],
                    launched_date=row["obj_source_launched"],
                    address=row["obj_source_address"],
                    e_power=row["obj_source_e_power"],
                    t_power=row["obj_source_t_power"],
                    boiler_count=row["obj_source_boiler_count"],
                    turbine_count=row["obj_source_turbine_count"],
                    geo_data=row["obj_source_coordinates"],
                ),
                update_fields=dict(
                    launched_date=row["obj_source_launched"],
                    address=row["obj_source_address"],
                    e_power=row["obj_source_e_power"],
                    t_power=row["obj_source_t_power"],
                    boiler_count=row["obj_source_boiler_count"],
                    turbine_count=row["obj_source_turbine_count"],
                    geo_data=row["obj_source_coordinates"],
                )
            )

            try:
                obj_source_station.consumer_stations.append(obj_consumer_station)
                session.commit()
            except Exception as e:
                session.rollback()

            material_wall = create_or_update(
                session=session,
                Model=MaterialWall,
                constraint="uni_material_walls_name",
                create_fields=dict(
                    name=row["wall_material"],
                    k=row["wall_material_k"],
                ),
                update_fields=dict(
                    k=row["wall_material_k"],
                )
            )

            # operation_mode, sock_type, obj_consumer_energy_class, priority

            obj_consumer = create_or_update(
                session=session,
                Model=ObjConsumer,
                constraint="uni_obj_consumers_address",
                create_fields=dict(
                    location_district_id=location_district.id,
                    location_area_id=location_area.id,
                    obj_consumer_station_id=obj_consumer_station.id,
                    address=row["obj_consumer_address"],
                    geo_data=row["obj_consumer_coordinates"],
                    temp_conditions=row["temp_conditions"],
                    street=row["obj_consumer_street"],
                    house_type=row["obj_consumer_house_type"],
                    house_number=row["obj_consumer_house_number"],
                    corpus_number=row["obj_consumer_corpus_number"],
                    soor_type=row["obj_consumer_soor_type"],
                    soor_number=row["obj_consumer_soor_number"],
                    balance_holder=row["obj_consumer_balance_holder"],
                    load_gvs=row["obj_consumer_gvs_load_avg"],
                    load_fact=row["obj_consumer_gvs_load_fact"],
                    heat_load=row["obj_consumer_heat_build_load"],
                    vent_load=row["obj_consumer_vent_build_load"],
                    total_area=row["obj_consumer_total_area"],
                    target=row["obj_consumer_target"],
                    b_class=row["obj_consumer_class"],
                    floors=row["obj_consumer_build_floors"],
                    # number=row["obj_source_address"],
                    wear_pct=row["obj_consumer_building_wear_pct"],
                    build_year=row["obj_consumer_build_date"],
                    type=row["obj_consumer_build_type"],
                    sock_type=row["sock_type"],
                    energy_class=row["obj_consumer_energy_class"],
                    operating_mode=row['operation_mode'],
                    priority=row['priority'],
                    is_dispatch=row["obj_consumer_is_dispatch"],
                ),
                update_fields=dict(
                    geo_data=row["obj_consumer_coordinates"],
                    temp_conditions=row["temp_conditions"],
                    street=row["obj_consumer_street"],
                    house_type=row["obj_consumer_house_type"],
                    house_number=row["obj_consumer_house_number"],
                    corpus_number=row["obj_consumer_corpus_number"],
                    soor_type=row["obj_consumer_soor_type"],
                    soor_number=row["obj_consumer_soor_number"],
                    balance_holder=row["obj_consumer_balance_holder"],
                    load_gvs=row["obj_consumer_gvs_load_avg"],
                    load_fact=row["obj_consumer_gvs_load_fact"],
                    heat_load=row["obj_consumer_heat_build_load"],
                    vent_load=row["obj_consumer_vent_build_load"],
                    total_area=row["obj_consumer_total_area"],
                    target=row["obj_consumer_target"],
                    b_class=row["obj_consumer_class"],
                    floors=row["obj_consumer_build_floors"],
                    # number=row["obj_source_address"],
                    wear_pct=row["obj_consumer_building_wear_pct"],
                    build_year=row["obj_consumer_build_date"],
                    type=row["obj_consumer_build_type"],
                    sock_type=row["sock_type"],
                    energy_class=row["obj_consumer_energy_class"],
                    operating_mode=row['operation_mode'],
                    priority=row['priority'],
                    is_dispatch=row["obj_consumer_is_dispatch"],
                )
            )

            try:
                obj_consumer.wall_material.append(material_wall)
                session.commit()
            except Exception as e:
                session.rollback()

            # events['unom'] = events['unom'].astype(int)
            events_df = events[events['unom'] == float(row['obj_consumer_unom'])]
            # if not events.empty:
            #     print(float(row['obj_consumer_unom']))
            # events_df = events[events['unom'] == float(row['obj_consumer_station_unom'])]
            # if not events.empty:
            #     print()

            for idx, e in events_df.iterrows():
                event_consumer = EventConsumer()
                event_consumer.obj_consumer_id = obj_consumer.id
                event_consumer.source = e['event_source']
                event_consumer.description = e['event_description']
                event_consumer.is_approved = True
                event_consumer.is_closed = True
                event_consumer.probability = 100.0
                event_consumer.days_of_work = e['days_of_work']
                event_consumer.created = e['event_created']
                event_consumer.closed = e['event_closed']
                session.add(event_consumer)

            counter_events_filtered = counter_events[counter_events['unom'] == float(row['obj_consumer_unom'])]
            ###
            # if not counter_events_filtered.empty:
            #     counter_events_filtered = counter_events_filtered[(counter_events_filtered['month_year'] >= e['event_created']) & (counter_events_filtered['month_year'] <= e['event_closed'])]
            #     if not counter_events_filtered.empty:
            #         print()
            ###
            for idx, ec in counter_events_filtered.iterrows():
                event_counter = EventCounter()
                event_counter.obj_consumer_id = obj_consumer.id
                # event_counter.event_consumer_id = ec['']
                event_counter.contour = ec['contour_co']
                event_counter.counter_mark = ec['counter_mark']
                event_counter.counter_number = ec['number_counter']
                event_counter.created = ec['month_year']
                event_counter.gcal_in_system = ec['obyom_podanogo_teplonositelya_v_sistemu_co']
                event_counter.gcal_out_system = ec['obyom_obratnogo_teplonositelya_is_sistemu_co']
                event_counter.subset = ec['podmes']
                event_counter.leak = ec['ytechka']
                event_counter.supply_temp = ec['temp_podachi']
                event_counter.return_temp = ec['temp_obratki']
                event_counter.work_hours_counter = ec['narabotka_chasov_schetchika']
                event_counter.heat_thermal_energy = ec['rashod_teplovoy_energy']
                event_counter.errors = ec['errors']
                event_counter.errors_desc = ec['error_desc']
                session.add(event_counter)
            session.commit()

    # @staticmethod
    # def save_wall_materials(session: Session, df: pd.DataFrame) -> pd.DataFrame:
    #     for index, row in df.iterrows():
    #         wall_materials = list(set(
    #             df['okrug_potrebitelja'].unique().tolist()
    #             + df['okrug_tstp_itp'].unique().tolist()
    #         ))


# сохранить без подгрузки координат
def save_for_view(session: Session, tables: dict):
    job = FakeJob.get_current_job()
    # df = tables.get("full")
    counter_events = tables.get("events_counter_all")
    events = tables.get("events_all")
    flat_table = tables.get("flat_table")
    # locations = SaveView.save_locations(session=session, df=df)
    SaveView.save_objects_new(session=session, df=flat_table, events=events, counter_events=counter_events)
    # SaveView.save_objects(session=session, df=flat_table, locations=locations, all_events=events)
    print('Success')


def save_for_predict(db: Engine, df_predict: pd.DataFrame):
    df_predict.to_sql(name="consumer_event_predict", con=db, if_exists="replace", index=False)


def save_predicated(session: Session, predicated_df: pd.DataFrame, events_df: pd.DataFrame):
    events_df.rename(columns={"id": "event_class"}, inplace=True)
    # predicated_df = predicated_df.join(events_df, on="event_id", how="inner")
    predicated_df = predicated_df.merge(events_df, on='event_class', how='inner')
    # ограничение по точности
    predicated_df = predicated_df[predicated_df['percent'] > 0.7]
    predicated_df.reset_index()
    for i, row in predicated_df.iterrows():
        event = EventConsumer()
        event.obj_consumer_id = row['obj_consumer_id']
        event.source = "Модель"
        event.is_closed = False
        event.description = row['event_name']
        event.created = datetime.datetime.now()
        event.probability = round(row['percent'], 2)
        event.is_approved = False
        session.add(event)
    session.commit()


def save_model_info(session: Session, model: CatBoostClassifier, accuracy_score: float, feature_importances: dict):
    model_info = ModelInfo(
        name="new_events_new_dsa.cbm",
        path="new_events_new_dsa.cbm",
        # path=os.getenv("MODEL_PATH") + "/events.cbm",
        metrics="",
        accuracy=round(accuracy_score, 2),
        feature_importance=feature_importances,
        created=datetime.datetime.now(),
    )
    session.add(model_info)
    session.commit()


def update_coordinates(session: Session):
    pass

# if __name__ == '__main__':
#     print()
#     df = pd.read_excel('test.xlsx', sheet_name='full')
#     save_for_view(df=df)
