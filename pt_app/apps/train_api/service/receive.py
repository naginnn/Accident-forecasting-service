import pandas as pd
from sqlalchemy import text as sa_text, select, Engine


def collect_data(db: Engine) -> pd.DataFrame:
    query = sa_text("SELECT * FROM obj_areas")
    df = pd.read_sql(query, con=db)
    return df


def predict_data(df: pd.DataFrame) -> pd.DataFrame:
    return df
