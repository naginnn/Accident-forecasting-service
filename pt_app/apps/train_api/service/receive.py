import os
from typing import Dict, Any, Iterator
from catboost import *
import pandas as pd
from pandas import DataFrame
# from settings.db import sync_db
from sqlalchemy import text as sa_text, select, Engine, inspect
from sqlalchemy.schema import CreateSchema
from transliterate import translit
import re
import numpy as np
from joblib import Parallel, delayed, parallel_backend
from sqlalchemy import create_engine
unprocessed_schema_name = "unprocessed"


# def save_unprocessed_data(db: Engine, files: dict) -> None:
#     """Сохранить не обработанные таблицы"""
#     with db.connect() as connection:
#         connection.execute(CreateSchema(unprocessed_schema_name, if_not_exists=True))
#         connection.commit()
#     reg = re.compile('[^a-zA-Z_ ]')
#     for file_name, file in files.items():
#         for sheet_name in file.sheet_names:
#             df = pd.read_excel(file, sheet_name=sheet_name)
#             df.columns = [reg.sub('', translit(column, 'ru', reversed=True).replace(" ", "_").lower()) for column in
#                           df.columns]
#             table_name = f"{file_name.split('.')[0].replace('-', '_')}_{sheet_name.replace('-', '_')}"
#             df.to_sql(name=table_name, con=db, if_exists="replace", schema=unprocessed_schema_name, index=False)
# files = None

def save_unprocessed_data(db: Engine, tables: dict) -> None:
    """Сохранить не обработанные таблицы"""
    # db = create_engine(conn_str)
    with db.connect() as connection:
        connection.execute(CreateSchema(unprocessed_schema_name, if_not_exists=True))
        connection.commit()
    # for table_name, table in tables.items():
    #     table.to_sql(name=table_name, con=db, if_exists="replace", schema=unprocessed_schema_name, index=False)
    conn_str = f'postgresql://{db.url.username}:{db.url.password}@{db.url.host}:{db.url.port}/{db.url.database}'
    Parallel(n_jobs=-2, verbose=10)(delayed(__save_unproc_table)
                                    (conn_str, table, table_name, unprocessed_schema_name)
                                    for table_name, table in tables.items())


def __save_unproc_table(conn_str: str, table: pd.DataFrame, name: str, schema: str, ):
    db = create_engine(conn_str)
    table.to_sql(name=name, con=db, if_exists="replace", schema=schema, index=False)


def __get_unproc_table(query: str, name: str):
    db = ""
    return {name: pd.read_sql(query, db)}


def get_unprocessed_data(db: Engine) -> dict[Any, DataFrame | Iterator[DataFrame]]:
    """Получить не обработанные таблицы"""
    inspector = inspect(db)
    table_names = inspector.get_table_names(schema=unprocessed_schema_name)
    tables = {}
    for table_name in table_names:
        query = sa_text(f"select * from {unprocessed_schema_name}.{table_name}")
        tables[table_name] = pd.read_sql(query, db)
    tables['event_types'] = pd.read_sql(sa_text(f"select * from public.event_types"), db)
    return tables


def get_processed_data(db: Engine) -> dict[str, DataFrame]:
    tables = {}

    def load(query: str) -> DataFrame:
        pass

    query = sa_text(f"""
    select
        oss.id obj_source_satation_id,
        oss.e_power, oss.t_power,
        oss.boiler_count, oss.turbine_count,
        -- oss.launched_date,
        oc.obj_consumer_station_id,
        oc.id obj_consumer_id,
        oc.load_gvs, oc.load_fact, oc.heat_load, oc.vent_load,
        oc.total_area,
        oc.location_district_id, oc.location_area_id,
        -- oc.address,
        oc.street, oc.house_number,
        -- oc.corpus_number, oc.soor_type, oc.soor_number,
        oc.b_class, oc.floors,
        oc.wear_pct,
        oc.build_year,
        oc.sock_type,
        oc.energy_class,
        oc.operating_mode,
        oc.priority,
        oc.is_dispatch
     from public.obj_consumers oc
     join public.obj_consumer_stations cs on oc.obj_consumer_station_id = cs.id
     join obj_source_consumer_stations ocs on oc.obj_consumer_station_id = ocs.obj_consumer_station_id
     join public.obj_source_stations oss on oss.id = ocs.obj_source_station_id
         """)
    tables["consumers"] = pd.read_sql(query, db)
    query = sa_text(f"select * from public.event_types")
    tables["events_classes"] = pd.read_sql(query, db)
    query = sa_text(f"select * from public.counter_consumer_events")
    tables["counter_consumer_events"] = pd.read_sql(query, db)
    return tables


def predict_data(model: CatBoostClassifier, predict_df: pd.DataFrame) -> pd.DataFrame:
    cl = model.classes_
    res2 = model.predict_proba(predict_df)
    all_result = {'event_class': [], 'percent': []}
    for r in res2:
        all_result['event_class'].append(cl[np.argmax(r)])
        all_result['percent'].append(r[np.argmax(r)])
        print()
    # res = model.predict(predict_df)
    predict_df["event_class"] = all_result['event_class']
    predict_df["percent"] = all_result['percent']
    predict_df = predict_df[predict_df['event_class'] != 0]
    return predict_df[['obj_consumer_id', "event_class", "percent"]]
