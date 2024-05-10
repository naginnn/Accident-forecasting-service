from typing import Dict, Any, Iterator
from catboost import *
import pandas as pd
from pandas import DataFrame
from sqlalchemy import text as sa_text, select, Engine, inspect
from sqlalchemy.schema import CreateSchema
from transliterate import translit
import re

unprocessed_schema_name = "unprocessed"


def save_unprocessed_data(db: Engine, files: dict) -> None:
    with db.connect() as connection:
        connection.execute(CreateSchema(unprocessed_schema_name, if_not_exists=True))
        connection.commit()
    reg = re.compile('[^a-zA-Z_ ]')
    for file_name, file in files.items():
        for sheet_name in file.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet_name)
            df.columns = [reg.sub('', translit(column, 'ru', reversed=True).replace(" ", "_").lower()) for column in
                          df.columns]
            table_name = f"{file_name.split('.')[0]}_{sheet_name}"
            df.to_sql(name=table_name, con=db, if_exists="replace", schema=unprocessed_schema_name, index=False)


def get_unprocessed_data(db: Engine) -> dict[Any, DataFrame | Iterator[DataFrame]]:
    """Получить не обработанные таблицы"""
    inspector = inspect(db)
    table_names = inspector.get_table_names(schema=unprocessed_schema_name)
    tables = {}
    for table_name in table_names:
        query = sa_text(f"select * from {unprocessed_schema_name}.{table_name}")
        tables[table_name] = pd.read_sql(query, db)
    return tables


def collect_data(db: Engine) -> pd.DataFrame:
    query = sa_text("SELECT * FROM obj_areas")
    df = pd.read_sql(query, con=db)
    return df


def predict_data(model: CatBoostClassifier, tables: dict) -> pd.DataFrame:
    df = tables.get("full")
    return df

