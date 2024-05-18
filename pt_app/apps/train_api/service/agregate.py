from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import re

from apps.train_api.service.utils import MultiColumnLabelEncoder

pd.options.mode.chained_assignment = None  # default='warn'


def agr_for_view(tables: dict) -> dict:
    """Агрегация данных"""
    agr_tables = {}
    df = tables.get('test_full')
    df = AgrView.get_ranking(df)
    df = AgrView.get_temp_conditions(df)
    df = AgrView.split_address(df)
    agr_tables["full"] = df
    agr_tables["events_all"] = tables.get('test_events_all')
    return agr_tables


def agr_for_train(tables: dict) -> tuple:
    df = tables.get('view_table')
    df = AgrTrain.agr_date(df)
    df = AgrTrain.get_work_class(df)
    # Преобразуем в числовые параметры
    df = MultiColumnLabelEncoder(columns=[
        'consumer_address', 'consumer_name',
    ]).fit_transform(df)
    print()

    agr_train_tables, agr_predict_tables = {}, {}
    agr_train_tables["full"] = tables.get('test_full')
    agr_predict_tables["full"] = tables.get('test_full')
    return agr_train_tables, agr_predict_tables


class AgrView:
    @staticmethod
    def get_ranking(df: pd.DataFrame) -> pd.DataFrame:
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
        return all_df

    @staticmethod
    def get_temp_conditions(df: pd.DataFrame) -> pd.DataFrame:
        df["temp_conditions"] = df["tip_obekta"].apply(lambda x: Utils.temp_conditions(x))
        return df

    @staticmethod
    def split_address(df: pd.DataFrame) -> pd.DataFrame:
        df['street'], df['house_number'], df['building'], df['section'] = \
            zip(*df['adres_potrebitelja'].map(Utils.parse_address))
        return df
        # df[df['street'].isnull()]


class AgrTrain:
    @staticmethod
    def agr_date(df: pd.DataFrame) -> pd.DataFrame:
        df['year'] = df['event_created'].dt.year
        df['month'] = df['event_created'].dt.month
        df['season'] = df['month'] % 12 // 3 + 1
        df['day'] = df['event_created'].dt.day
        df['work_time'] = (df['event_closed'] - df['event_created']).dt.days
        df['day_of_week'] = df['event_created'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        return df

    @staticmethod
    def get_work_class(df: pd.DataFrame) -> pd.DataFrame:
        events = [
            "P1 <= 0",
            "P2 <= 0",
            "T1 > max",
            "T1 < min",
            "Авария",
            "Недостаточная температура подачи ЦО (Недотоп)",
            "Превышение температуры подачи ЦО (Перетоп)",
            "Утечка теплоносителя",
            "Течь в системе отопления",
            "Температура в квартире ниже нормативной",
            "Отсутствие отопления в доме",
            "Сильная течь в системе отопления",
            "Крупные пожары",
            "Температура в помещении общего пользования ниже нормативной",
            "Аварийная протечка труб в подъезде",
            "Протечка труб в подъезде",
            "Температура в помещении общего пользования ниже нормативной",
            "Отсутствие отопления в доме",
            "Температура в квартире ниже нормативной",
            "Течь в системе отопления",
            "Сильная течь в системе отопления",
        ]
        df["accident"] = df["event_name"].apply(lambda x: Utils.put_down_class(x, events))
        return df


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

    @staticmethod
    def temp_conditions(x):
        match x:
            case "Социальный":
                return dict(
                    summer_high=25.0,
                    summer_low=22.0,
                    winter_high=22.0,
                    winter_low=20.0,
                )
            case "МКД":
                return dict(
                    summer_high=22.0,
                    summer_low=20.0,
                    winter_high=20.0,
                    winter_low=18.0,
                )
            case "Индустриальный":
                return dict(
                    summer_high=20.0,
                    summer_low=18.0,
                    winter_high=21.0,
                    winter_low=19.0,
                )
            case _:
                return dict(
                    summer_high=22.0,
                    summer_low=20.0,
                    winter_high=20.0,
                    winter_low=18.0,
                )

        # match x:
        #     case "Детский сад":
        #         return dict(summer=22.0, winter=20.0)
        #     case "Школа":
        #         return dict(summer=22.0, winter=20.0)
        #     case "Поликлиника":
        #         return dict(summer=22.0, winter=20.0)
        #     case "Теарт":
        #         return dict(summer=22.0, winter=20.0)
        #     case "Колледж":
        #         return dict(summer=22.0, winter=20.0)
        #     case _:
        #         return dict(summer=18.0, winter=18.0)

    @staticmethod
    def parse_address(x):
        new_xxx = [xx.strip() for xx in x.strip().split(",")]
        address = [new_xxx.pop(0), None, None, None]
        new_xxx = [xx.replace(" ", "") for xx in new_xxx]
        for new_x in new_xxx:
            if "д." in new_x or "вл." in new_x:
                address[1] = new_x.split('.')[-1]
            elif "к." in new_x or "корп." in new_x:
                address[2] = new_x.split('.')[-1]
            elif "с." in new_x or "стр." in new_x:
                address[3] = new_x.split('.')[-1]
        return address

        # return [street, house_number, building, section]

    @staticmethod
    def put_down_class(x: str, events: list) -> int:
        if x in events:
            return 1
        return 0

    @staticmethod
    def parse_date(x: str):
        pass
