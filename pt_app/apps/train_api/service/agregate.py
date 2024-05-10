from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def agr_for_view(tables: dict) -> dict:
    """Агрегация данных"""
    agr_tables = {}
    df = tables.get('test_full')
    print(df.columns)
    # df = pd.read_excel(df_all.get("test.xlsx"), sheet_name='full')
    df['work_time_prior'] = df['vremja_raboty'].apply(lambda x: Utils.priority(x))
    df['build_type_prior'] = df['tip_obekta'].apply(lambda x: Utils.priority(x))
    df['energy_prior'] = df['klass_energ_eff'].apply(lambda x: Utils.priority(x))
    consumer_sources = df['adres_tstp_itp'].unique().tolist()
    all_df = pd.DataFrame()
    for source in consumer_sources:
        new_df = df[df['adres_tstp_itp'] == source]
        new_df['work_time_prior_rank'] = new_df[['work_time_prior']].apply(tuple, axis=1) \
            .rank(method='min', ascending=True).astype(int)
        new_df['build_type_prior_rank'] = new_df[['build_type_prior']].apply(tuple, axis=1) \
            .rank(method='min', ascending=True).astype(int)
        new_df['energy_prior_rank'] = new_df[['energy_prior']].apply(tuple, axis=1) \
            .rank(method='min', ascending=True).astype(int)
        new_df['priority'] = new_df['work_time_prior_rank'] + new_df['build_type_prior_rank'] + new_df[
            'energy_prior_rank']
        new_df.sort_values(["priority", "adres_tstp_itp"], inplace=True, ascending=True)
        all_df = pd.concat([all_df, new_df])
    all_df = all_df.drop(['work_time_prior_rank', 'build_type_prior_rank', 'energy_prior_rank',
                          'work_time_prior', 'build_type_prior', 'energy_prior'], axis=1)
    agr_tables["full"] = all_df
    return agr_tables


def agr_for_train(tables: dict) -> tuple:
    agr_train_tables, agr_predict_tables = {}, {}
    agr_train_tables["full"] = tables.get('test_full')
    agr_predict_tables["full"] = tables.get('test_full')
    return agr_train_tables, agr_predict_tables


class Utils:
    @staticmethod
    def priority(x):
        match x:
            case 'Круглосуточно':
                return 1
            case '9:00 - 21:00':
                return 2
            case '9:00 – 18:00':
                return 3
            case 'A':
                return 1
            case 'B':
                return 2
            case 'C':
                return 3
            case 'Социальный':
                return 1
            case 'Индустриальный':
                return 2
            case 'МКД':
                return 3
            case _:
                return 3
