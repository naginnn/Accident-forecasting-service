import datetime
import pandas as pd
from apps.train_api.src._test_utils import log


pd.options.mode.chained_assignment = None  # default='warn'


class AgrTrain:
    @staticmethod
    @log
    def execute(tables: dict) -> tuple:
        df = tables.get('view_table')
        events_df = tables.get('event_types')
        df = AgrTrain._agr_date(df)
        df = AgrTrain._get_work_class(df, events_df)
        # df = AgrTrain.get_work_classes_all(df)
        # Преобразуем в числовые параметры
        # close time не учитывать при обучении, интервал тоже
        df = AgrTrain._clear_data(df)

        # df = MultiColumnLabelEncoder(columns=[
        #     'consumer_address', 'consumer_name',
        # ]).fit_transform(df)
        agr_train_df = AgrTrain._get_train_data(df)
        agr_predict_df = AgrTrain._get_predict_data(agr_train_df)
        agr_train_df.to_csv("agr_train_df.csv", index=False)
        agr_predict_df.to_csv("agr_predict_df.csv", index=False)
        # agr_train_tables["full"] = tables.get('test_full')
        # agr_predict_tables["full"] = tables.get('test_full')
        return agr_predict_df, agr_train_df

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
