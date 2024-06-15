import datetime
import pandas as pd
from apps.train_api.src._test_utils import log
from apps.train_api.service.utils import MultiColumnLabelEncoder

pd.options.mode.chained_assignment = None  # default='warn'


class AgrTrain:
    @staticmethod
    @log
    def execute(tables: dict) -> tuple:
        consumers = tables.get("consumers")
        events_classes = tables.get("events_classes")
        counter_consumer_events = tables.get("counter_consumer_events")

        counter_consumer_events['time'] = counter_consumer_events.apply(
            lambda x: AgrTrain._set_date(x), axis=1)
        counter_consumer_events.reset_index()
        events_classes = events_classes.set_index('event_name').T.to_dict(
            'index').get('id')
        keys = list(events_classes.keys())
        counter_consumer_events['event_class'] = counter_consumer_events[
            'description'].apply(
            lambda x: AgrTrain._set_event_class(x, events_classes, keys))
        counter_consumer_events.drop(
            columns=['id_y', 'id_x', 'index', 'id', 'description',
                     'counter_event_created', 'event_created', 'event_closed',
                     'errors_desc'], inplace=True, axis=1)
        counter_consumer_events = AgrTrain._split_date(counter_consumer_events)
        agr_events = AgrTrain._compare_events(counter_consumer_events)
        consumers = AgrTrain._transform_consumer(consumers)
        train_df = pd.merge(consumers, agr_events, how='left',
                            on='obj_consumer_id')
        train_df = train_df[['obj_source_satation_id',
                             'e_power',
                             't_power',
                             'boiler_count',
                             'turbine_count',
                             'obj_consumer_station_id',
                             'obj_consumer_id',
                             'load_gvs',
                             'load_fact',
                             'heat_load',
                             'vent_load',
                             'total_area',
                             'location_district_id',
                             'location_area_id',
                             'street',
                             'house_number',
                             'b_class',
                             'floors',
                             'wear_pct',
                             'build_year',
                             'sock_type',
                             'energy_class',
                             'operating_mode',
                             'priority',
                             'is_dispatch',
                             'gcal_in_system',
                             'gcal_out_system',
                             'subset',
                             'leak',
                             'supply_temp',
                             'return_temp',
                             'heat_thermal_energy',
                             'errors',
                             'days_of_work',
                             'time',
                             'year',
                             'month',
                             'season',
                             'day',
                             'day_of_week',
                             'is_weekend',
                             'last_event_class',
                             'last_event_days',
                             'event_class', ]]
        agr_train_df = train_df[train_df['last_event_class'].notna()]

        agr_train_df.dropna(inplace=True)

        agr_predict_df = train_df.groupby(['obj_consumer_id']).first()
        agr_predict_df = agr_predict_df.reset_index()
        agr_predict_df['time'] = datetime.datetime.now()
        agr_predict_df['time'] = agr_predict_df['time'].astype(
            'datetime64[ns]')
        # ss['time'] = ss['time'].apply(lambda x: x + pd.Timedelta("1 day"))
        agr_predict_df = AgrTrain._split_date(agr_predict_df)
        agr_predict_df['last_event_days'] = agr_predict_df.apply(
            lambda x: x['last_event_days'] if x['event_class'] == 0 else 0,
            axis=1)
        agr_predict_df['last_event_class'] = agr_predict_df.apply(
            lambda x: x['event_class'], axis=1)
        agr_predict_df['event_class'] = 0
        agr_predict_df.sort_values(by=['leak'], ascending=True,
                                   na_position='last', inplace=True)
        agr_predict_df.interpolate(method='linear', inplace=True)
        agr_predict_df.sort_values(by=['obj_consumer_id'], ascending=True,
                                   inplace=True)

        agr_train_df.drop('time', inplace=True, axis=1)
        agr_predict_df.drop(columns=['time', 'event_class'], inplace=True,
                            axis=1)

        return agr_predict_df, agr_train_df

    @staticmethod
    @log
    def execute_predict(custom: bool = False):
        if custom:
            pass
            return
        pass

    @staticmethod
    def _transform_consumer(df: pd.DataFrame) -> pd.DataFrame:
        df = MultiColumnLabelEncoder(columns=[
            'street', 'house_number',
            'b_class', 'sock_type', 'energy_class',
            'operating_mode',
        ]).fit_transform(df)
        return df

    @staticmethod
    def _compare_events(events: pd.DataFrame):
        consumers = events['obj_consumer_id'].unique().tolist()
        events['last_event_class'] = 0
        events['last_event_days'] = 0
        # df['between_created'] = 0
        train_df = pd.DataFrame()
        # last = 0
        for consumer in consumers:
            consumers_df = events[events['obj_consumer_id'] == consumer].sort_values(by='time', ascending=True)
            consumers_df = consumers_df.reset_index()
            last_event_class = 0
            last_event_day = 0
            for i, row in consumers_df.iterrows():
                if i > 0:
                    if consumers_df.at[i - 1, 'event_class'] != 0:
                        last_event_class = consumers_df.at[i - 1, 'event_class']
                        last_event_day = consumers_df.at[i, 'time']
                    # abs((df['event_closed'] - df['event_created']).dt.days.astype(float))
                    consumers_df.at[i, 'last_event_class'] = last_event_class
                    if last_event_day != 0:
                        consumers_df.at[i, 'last_event_days'] = (consumers_df.at[i, 'time'] - last_event_day).days
                else:
                    consumers_df.at[i, 'last_event_days'] = 0
                    consumers_df.at[i, 'last_event_class'] = 0
                    # consumers_df.at[i, 'last_event_class'] = last
            # consumers_df = consumers_df[(consumers_df['event_class'] != 0) | (consumers_df['last_event_class'] != 0)]
            train_df = pd.concat([train_df, consumers_df])
        train_df = train_df.sort_values(by=['obj_consumer_id', 'time'], ascending=(True, False))
        train_df.fillna({
            'gcal_in_system': 0,
            'gcal_out_system': 0,
            'subset': 0,
            'leak': 0,
            'supply_temp': 0,
            'return_temp': 0,
            'heat_thermal_energy': 0,
            'days_of_work': 0,
            'errors': 0,
        }, inplace=True)
        train_df['errors'] = train_df['errors'].apply(lambda x: len(x.split(',')) if x != 0 else 0)
        train_df.drop('index', inplace=True, axis=1)
        return train_df

    @staticmethod
    def _split_date(events: pd.DataFrame):
        events['year'] = events['time'].dt.year
        events['month'] = events['time'].dt.month
        events['season'] = events['month'] % 12 // 3 + 1
        events['day'] = events['time'].dt.day
        # df['work_time'] = (df['event_closed'] - df['event_created']).dt.days
        events['day_of_week'] = events['time'].dt.dayofweek
        events['is_weekend'] = events['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        return events

    # Utils
    @staticmethod
    def _set_date(x):
        if not pd.isnull(x['counter_event_created']):
            return x['counter_event_created']
        if not pd.isnull(x['event_created']):
            return x['event_created']
        if not pd.isnull(x['event_closed']):
            return x['event_closed']

    @staticmethod
    def _set_event_class(x, events_classes: dict, keys: list):
        if x in keys:
            return events_classes.get(x)
        # return 1
        return 0

    @staticmethod
    @log
    def _agr_date(df: pd.DataFrame) -> pd.DataFrame:
        df['year'] = df['event_created'].dt.year
        df['month'] = df['event_created'].dt.month
        df['season'] = df['month'] % 12 // 3 + 1
        df['day'] = df['event_created'].dt.day
        # df['work_time'] = (df['event_closed'] - df['event_created']).dt.days
        df['day_of_week'] = df['event_created'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        return df

    @staticmethod
    @log
    def _get_work_class(df: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
        events = events.set_index('event_name').T.to_dict('index').get('id')
        keys = list(events.keys())
        df["accident"] = df["event_description"].apply(lambda x: AgrTrain._put_down_class(x, events, keys))
        return df

    @staticmethod
    @log
    def _get_work_classes_all(df: pd.DataFrame) -> pd.DataFrame:
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
        df["accident"] = df["event_name"].apply(lambda x: AgrTrain._check_in_type(x, alpabet))
        return df

    @staticmethod
    @log
    def _clear_data(df: pd.DataFrame) -> pd.DataFrame:
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
    @log
    def _get_predict_data(df: pd.DataFrame) -> pd.DataFrame:
        time_now = datetime.datetime.now()
        df_predict = df.groupby("consumer_id", as_index=False).last(True)  # 83125
        df_predict['last_event_id'] = df_predict['event_id']
        # # between block
        # df_predict['event_created'] = df_predict.apply(lambda x: Utils.collect_the_date(x), axis=1)
        # df_predict['between_created'] = df_predict['event_created'].apply(lambda x: (time_now - x).days)
        # # between block

        df_predict['event_created'] = time_now
        df_predict = AgrTrain._agr_date(df_predict)

        df_predict = df_predict.drop(columns='event_created')
        df_predict = df_predict[df.columns.tolist()]
        df_predict = df_predict.drop(columns='event_id')
        return df_predict

    @staticmethod
    @log
    def _get_train_data(df: pd.DataFrame) -> pd.DataFrame:
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

    @staticmethod
    def _put_down_class(x: str, events: dict, keys: list) -> int:
        if x in keys:
            return events.get(x)
            # return 1
        return 0

    @staticmethod
    def _check_in_type(x: str, alpabet: dict) -> int:
        alpabet.keys()
        scores = {}
        for k, v in alpabet.items():
            for tp in v:
                if not isinstance(x, str) or x == '':
                    scores['Другое'] = scores['Другое'] + 1 if scores.get('Другое') else 1
                    continue
                if tp in x:
                    if scores.get(k):
                        scores[k] += 1
                    else:
                        scores[k] = 1
        # print('Очки', scores)
        if scores:
            # return max(scores, key=scores.get)
            res = max(scores, key=scores.get)
            if res == 'Другое':
                return 30
            return list(alpabet.keys()).index(res)
        else:
            return -1
