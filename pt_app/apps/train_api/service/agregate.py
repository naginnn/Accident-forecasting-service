import datetime
from typing import Tuple
import numpy as np
from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import re

from apps.train_api.service.utils import MultiColumnLabelEncoder

pd.options.mode.chained_assignment = None  # default='warn'


def agr_for_view(tables: dict) -> dict:
    """Агрегация данных"""
    agr_tables = {}
    df_wall_materials = tables.get("test_wall_materials")
    df_full = tables.get('test_full')
    df_full = AgrView.get_ranking(df_full)
    df_full = AgrView.get_temp_conditions(df_full)
    df_full = AgrView.split_address(df_full)
    df_full = AgrView.split_wall_materials(df_full, df_wall_materials)
    df_events = tables.get('test_events_all')
    df_events = AgrView.get_work_days(df_events)
    agr_tables["full"] = df_full
    agr_tables["events_all"] = df_events

    return agr_tables


def agr_for_train(tables: dict) -> tuple:
    df = tables.get('view_table')
    events_df = tables.get('event_types')
    df = AgrTrain.agr_date(df)
    df = AgrTrain.get_work_class(df, events_df)
    # df = AgrTrain.get_work_classes_all(df)
    # Преобразуем в числовые параметры
    # close time не учитывать при обучении, интервал тоже
    df = AgrTrain.clear_data(df)

    # df = MultiColumnLabelEncoder(columns=[
    #     'consumer_address', 'consumer_name',
    # ]).fit_transform(df)
    agr_train_df = AgrTrain.get_train_data(df)
    agr_predict_df = AgrTrain.get_predict_data(agr_train_df)
    agr_train_df.to_csv("agr_train_df.csv", index=False)
    agr_predict_df.to_csv("agr_predict_df.csv", index=False)
    # agr_train_tables["full"] = tables.get('test_full')
    # agr_predict_tables["full"] = tables.get('test_full')
    return agr_predict_df, agr_train_df


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

    @staticmethod
    def get_work_days(df: pd.DataFrame) -> pd.DataFrame:
        df['days_of_work'] = (df['close_date'] - df['create_date']).dt.days.astype(float)
        return df

    @staticmethod
    def split_wall_materials(df: pd.DataFrame, df_wall_materials: pd.DataFrame) -> pd.DataFrame:
        df_wall_materials = df_wall_materials.rename(columns={"id": "material_sten", "name": "wall_material_description"})
        return df.merge(df_wall_materials, how='left', on='material_sten')


class AgrTrain:
    @staticmethod
    def agr_date(df: pd.DataFrame) -> pd.DataFrame:
        df['year'] = df['event_created'].dt.year
        df['month'] = df['event_created'].dt.month
        df['season'] = df['month'] % 12 // 3 + 1
        df['day'] = df['event_created'].dt.day
        # df['work_time'] = (df['event_closed'] - df['event_created']).dt.days
        df['day_of_week'] = df['event_created'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        return df

    @staticmethod
    def get_work_class(df: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
        events = events.set_index('event_name').T.to_dict('index').get('id')
        keys = list(events.keys())
        df["accident"] = df["event_description"].apply(lambda x: Utils.put_down_class(x, events, keys))
        return df

    @staticmethod
    def get_work_classes_all(df: pd.DataFrame) -> pd.DataFrame:
        alpabet = {
            'СК': ['строительный', 'контроль', 'ск'],
            'МОЭК': [
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
            ],
            'Подъезд': ['подъездов,', 'подъезд', 'инвалид', 'инвалид', 'полос', 'почтовый', 'почтовых',
                        'входной двери', 'входная дверь', 'панельных швов', 'панельные швы', 'отделочных', 'отделка',
                        'пандус', 'светильник'],
            'Окна': ['оконных', 'окна', 'окно'],
            'Проведение экспертизы': ['проведение', 'экспертизы', 'проектной', 'документации', 'проведение экспертизы'],
            'ПСД': ['проектная', 'проектной', 'документации', 'документация', 'псд'],
            'ЦО-М': ['теплоснабжения', 'цо-м', 'теплоснабжение', 'тепло', 'отопление', 'отопления'],
            'КАН-М': ['водоотведения', 'водоотведение', 'канализации', 'канализация', 'трубопроводы', 'кан-м',
                      'воды', 'вода', 'трубопровод', 'колодца', 'подтопление', 'подтопления'],
            'ГВС-М': ['горячего', 'горячее', 'водоснабжения', 'водоснабжение', 'гвс-м'],
            'ХВС-М': ['холодного', 'холодное', 'водоснабжения', 'водоснабжение', 'хвс-м'],
            'Мусоропровод': ['мусоропровода', 'мусоропровод', 'мусор'],
            'ПВ': ['пожарного', 'пожарный', 'водопровода', 'водопровод', 'пв'],
            'ППАиДУ': ['дым', 'внутридомовой', 'системы', 'дымоудаления', 'противопожарной', 'автоматики', 'ппаиду',
                       'пожарной'],
            'ЭС': ['электроснабжения', 'проводка', 'проводка', 'эс', 'электро', 'электропроводка', 'электропроводки'],
            'ГАЗ': ['газоснабжения', 'газоснабжение', 'газ', 'ковера', 'ковер'],
            'Подвал': ['подвальных', 'подвальный', 'подвал'],
            'ЦО': ['теплоснабжения', 'тепло', 'стояки', 'цо'],
            'КАН': ['водоотведения', 'водоотведение', 'канализации', 'канализация', 'кан', 'колодцы', 'колодец',
                    'засоры', 'засор'],
            'ГВС': ['горячего', 'горячее', 'горячий', 'водоснабжения', 'водоснабжениие', 'гвс'],
            'Фундамент': ['фундамента', 'фундамент'],
            'ХВС': ['холодного', 'водоснабжения', 'водоснабжение', 'хвс'],
            'Крыша': ['крыши', 'крыша', 'кровля', 'кровли'],
            'ВДСК': ['водостока', 'водосток', 'вдск'],
            'Балкон': ['балконов', 'балкон', 'балконы'],
            'Фасад': ['фасада', 'фасад', 'фасадов', 'фасады'],
            'Разработка и проведение экспертизы ПД, в том числе АН за проведением работ по сохранению ОКН, выявленных ОКН, научное руководство проведением указанных работ в случае проведения работ по КР ОИ в МКД  г. Москвы, являющихся ОКН, выявленными ОКН.':
                ['разработка', 'проведение', 'экспертизы', 'числе', 'проведением', 'работ', 'сохранению', 'окн,',
                 'выявленных', 'окн,', 'научное', 'руководство', 'проведением', 'указанных', 'работ', 'случае',
                 'проведения', 'работ', 'москвы,', 'являющихся', 'окн,', 'выявленными', 'окн.',
                 'разработка и проведение экспертизы пд, в том числе ан за проведением работ по сохранению окн, выявленных окн, научное руководство проведением указанных работ в случае проведения работ по кр ои в мкд  г. москвы, являющихся окн, выявленными окн.'],
            'Авторский надзор': ['авторский', 'надзор', 'авторский надзор'],
            'ПСД лифты': ['разработка', 'проектной', 'документации', 'лифтам', 'псд лифты'],
            'Лифт': ['лифтового', 'оборудования', 'лифт', 'лифты'],
            'Телемеханика': ['нет связи с пу', 'отсутствуют ',
                             'актуальные', 'значения', 'dsa',
                             'успд', 'угроза', 'взрыв', 'устройства', 'устройство', 'аномальное', 'значение',
                             'связь', 'связи', 'вибрации', 'датчик', 'интегральные', 't1', 'p1', 'p2', 'расхождение',
                             'расхождения', 'gsm'],
            'Освещение': ['освещения', 'освещение']}
        df["accident"] = df["event_name"].apply(lambda x: Utils.check_in_type(x, alpabet))
        return df

    @staticmethod
    def clear_data(df: pd.DataFrame) -> pd.DataFrame:
        df.drop([
            'consumer_address',
            'consumer_name',
            'event_description',
            # 'event_created',
            'event_closed',
            # 'event_id',
        ], axis=1, inplace=True)
        return df

    @staticmethod
    def get_predict_data(df: pd.DataFrame) -> pd.DataFrame:
        time_now = datetime.datetime.now()
        df_predict = df.groupby("consumer_id", as_index=False).last(True)  # 83125
        df_predict['last_event_id'] = df_predict['event_id']
        # # between block
        # df_predict['event_created'] = df_predict.apply(lambda x: Utils.collect_the_date(x), axis=1)
        # df_predict['between_created'] = df_predict['event_created'].apply(lambda x: (time_now - x).days)
        # # between block

        df_predict['event_created'] = time_now
        df_predict = AgrTrain.agr_date(df_predict)

        df_predict = df_predict.drop(columns='event_created')
        df_predict = df_predict[df.columns.tolist()]
        df_predict = df_predict.drop(columns='event_id')
        return df_predict

    @staticmethod
    def get_train_data(df: pd.DataFrame) -> pd.DataFrame:
        df['event_id'] = df['accident']
        consumers = df['consumer_id'].unique().tolist()
        df['last_event_id'] = 0
        # df['between_created'] = 0
        train_df = pd.DataFrame()
        last = 0
        for consumer in consumers:
            consumers_df = df[df['consumer_id'] == consumer].sort_values(by='event_created', ascending=True)
            consumers_df = consumers_df.reset_index()
            for i, row in consumers_df.iterrows():
                if i > 0:
                    last = consumers_df.at[i - 1, 'event_id']
                    consumers_df.at[i, 'last_event_id'] = last
                else:
                    consumers_df.at[i, 'last_event_id'] = last
            consumers_df = consumers_df[(consumers_df['event_id'] != 0) | (consumers_df['last_event_id'] != 0)]
            # consumers_df['event_count'] = np.arange(len(consumers_df)) + 1
            # # between block
            # consumers_df = consumers_df.reset_index()
            # for i, row in consumers_df.iterrows():
            #     if i > 0:
            #         last = consumers_df.at[i - 1, 'event_id']
            #         consumers_df.at[i, 'between_created'] = (
            #                     consumers_df.at[i, 'event_created'] - consumers_df.at[i - 1, 'event_created']).days
            #     else:
            #         consumers_df.at[i, 'between_created'] = 0
            # # between block
            train_df = pd.concat([train_df, consumers_df])
        train_df.drop([
            'index',
            'event_created',
            'accident',
            # 'level_0',
            # 'between_created',
        ], axis=1, inplace=True)
        train_df.dropna(axis=0, how='any', inplace=True)
        return train_df


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
    def put_down_class(x: str, events: dict, keys: list) -> int:
        if x in keys:
            return events.get(x)
            # return 1
        return 0

    @staticmethod
    def collect_the_date(x):
        return datetime.datetime(int(x['year']), int(x['month']), int(x['day']))

    # @staticmethod
    # def put_down_class(x: str, events: list) -> int:
    #     if x in events:
    #         return 1
    #     return 0
    #
    # @staticmethod
    # def check_in_type(x: str, alpabet: dict) -> int:
    #     alpabet.keys()
    #     scores = {}
    #     for k, v in alpabet.items():
    #         for tp in v:
    #             if not isinstance(x, str) or x == '':
    #                 scores['Другое'] = scores['Другое'] + 1 if scores.get('Другое') else 1
    #                 continue
    #             if tp in x:
    #                 if scores.get(k):
    #                     scores[k] += 1
    #                 else:
    #                     scores[k] = 1
    #     # print('Очки', scores)
    #     if scores:
    #         # return max(scores, key=scores.get)
    #         res = max(scores, key=scores.get)
    #         if res == 'Другое':
    #             return 30
    #         return list(alpabet.keys()).index(res)
    #     else:
    #         return -1
