from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd


def agr_for_view(session: Session, df_all: dict):
    pass


def agr_for_model(session: Session, df: pd.DataFrame):
    pass
