from typing import Dict, Any, Iterator
from catboost import *
import pandas as pd
from pandas import DataFrame
from sqlalchemy import text as sa_text, select, Engine, inspect
from sqlalchemy.schema import CreateSchema
from transliterate import translit
import re
import numpy as np

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
    with db.connect() as connection:
        connection.execute(CreateSchema(unprocessed_schema_name, if_not_exists=True))
        connection.commit()
    for table_name, table in tables.items():
        table.to_sql(name=table_name, con=db, if_exists="replace", schema=unprocessed_schema_name, index=False)


def get_unprocessed_data(db: Engine) -> dict[Any, DataFrame | Iterator[DataFrame]]:
    """Получить не обработанные таблицы"""
    inspector = inspect(db)
    table_names = inspector.get_table_names(schema=unprocessed_schema_name)
    tables = {}
    for table_name in table_names:
        query = sa_text(f"select * from {unprocessed_schema_name}.{table_name}")
        tables[table_name] = pd.read_sql(query, db)
    return tables


def get_processed_data(db: Engine) -> dict[str, DataFrame]:
    tables = {}
    query = sa_text(f"""select
    ss.id source_station_id,
    cs.id cs_id, cs.location_district_id cs_location_district_id, cs.location_area_id cs_location_area_id,
    c.location_district_id c_district_id, c.location_area_id c_location_area_id, c.id consumer_id,
     c.name consumer_name, c.address consumer_address, c.total_area, c.living_area, c.not_living_area,
     c.priority,
    ec.id event_id, ec.description event_description, ec.created event_created, ec.closed event_closed, ec.days_of_work days_of_work
from obj_consumers as c
         join public.location_districts ld on ld.id = c.location_district_id
         join public.location_areas la on ld.id = c.location_area_id
         join public.obj_consumer_stations cs on cs.id = c.obj_consumer_station_id
         join public.obj_source_consumer_stations scs on cs.id = scs.obj_consumer_station_id
         join public.obj_source_stations ss on ss.id = scs.obj_source_station_id
         left join public.event_consumers ec on c.id = ec.obj_consumer_id
--          where ec.description in (select et.event_name from public.event_types et)
         """)
    tables["view_table"] = pd.read_sql(query, db)
    query = sa_text(f"select * from public.event_types")
    tables["event_types"] = pd.read_sql(query, db)
    return tables


def collect_data(db: Engine) -> pd.DataFrame:
    query = sa_text("SELECT * FROM public.obj_areas")
    df = pd.read_sql(query, con=db)
    return df


def predict_data(model: CatBoostClassifier, predict_df: pd.DataFrame) -> pd.DataFrame:
    cl = model.classes_
    res2 = model.predict_proba(predict_df)
    all_result = {'event_id': [], 'percent': []}
    for r in res2:
        all_result['event_id'].append(cl[np.argmax(r)])
        all_result['percent'].append(r[np.argmax(r)])
        print()
    # res = model.predict(predict_df)
    predict_df["event_id"] = all_result['event_id']
    predict_df["percent"] = all_result['percent']
    predict_df = predict_df[predict_df['event_id'] != 0]
    return predict_df[['consumer_id', "event_id", "percent"]]
