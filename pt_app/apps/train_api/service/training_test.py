import pandas as pd
import numpy as np
from sklearn import preprocessing
from rq.job import Job, get_current_job
from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session

from apps.train_api.service.agregate import agr_for_view, agr_for_model
from apps.train_api.service.receive import collect_data, predict_data
from apps.train_api.service.update import save_for_view, save_for_predict
from apps.train_api.service.utils import (get_word, MultiColumnLabelEncoder,
                                          reverse_date, check_in_type, alpabet)
from models.objects import ObjConsumerWeather, ObjDistrict, ObjArea
from pkg.utils import FakeJob
from pkg.ya_api import get_one_coordinate
from settings.db import DB_URL, get_sync_session, sync_db as db


def prepare_dataset(files: dict = None):
    job = FakeJob.get_current_job()
    session = get_sync_session()
    if files:
        df = agr_for_view(session=session, df_all=files)
        save_for_view(session=session, df=df)

    df = collect_data(db=db)
    df = agr_for_model(session=session, df=df)
    save_for_predict(session=session, df=df)
    predict_data(df=df)

    drop_weather_data(session=session)
    session.commit()
    pass

    # job = get_current_job()

    # try:
    df = pd.read_excel(files.get('1.xlsx'), sheet_name='Sheet1')
    job.meta['stage'] = 30
    job.save_meta()
    # чистка
    df.drop([
        'LOGIN', 'COL_755',
        'COL_754', 'COL_765', 'COL_2156',
        'COL_103506', 'PARENT_ID',
    ], axis=1, inplace=True)
    df = df[1:]
    # pd.options.mode.chained_assignment = None
    df.loc[:, 'COL_3468'] = df['COL_3468'].astype('str').apply(lambda x: get_word(x))
    # Преобразуем в числовые параметры
    df = MultiColumnLabelEncoder(columns=[
        'COL_757', 'COL_763', 'COL_764',
        'COL_766', 'COL_767', 'COL_772',
        'COL_775', 'COL_781', 'COL_2463',
        'COL_3468', 'COL_762',
    ]).fit_transform(df)
    # Чистка
    df.fillna({
        'COL_758': 0, 'COL_759': 0, 'COL_760': 0,
        'COL_761': 0, 'COL_770': 0, 'COL_771': 0,
        'COL_2463': 0, 'COL_3243': 0, 'COL_3363': 0,
    }, inplace=True)
    # Выделяем связь с инцидентами
    df.rename({
        'COL_782': 'UNOM',
    }, axis=1, inplace=True)

    ############### 2.xlsx
    # открываем файл с инцидентами лист 1
    work_types = pd.read_excel(files.get('2.xlsx'), sheet_name='Result 1')
    job.meta['stage'] = 40
    job.save_meta()
    # открываем файл с инцидентами лист 2
    work_types2 = pd.read_excel(files.get('2.xlsx'), sheet_name='Result 2')
    job.meta['stage'] = 50
    job.save_meta()

    # Матчим листы и приводим к единому виду
    work_types = pd.concat([work_types, work_types2])
    work_types['Дата создания во внешней системе'] = work_types['Дата создания во внешней системе'].str.lower()
    work_types['Дата закрытия'] = work_types['Дата закрытия'].str.lower()
    work_types['Дата создания во внешней системе'].fillna('01-01-1970 ', inplace=True)
    work_types['Дата закрытия'].fillna('01-01-1970 ', inplace=True)
    work_types['Дата создания во внешней системе'] = (
        work_types['Дата создания во внешней системе'].apply(lambda x: x.split(' ')[0].replace('-', '.')))
    work_types['Дата закрытия'] = (work_types['Дата закрытия'].apply(lambda x: x.split(' ')[0].replace('-', '.')))
    work_types.rename({
        'Наименование': 'WORK_NAME',
        'Дата создания во внешней системе': 'CREATE_DATE',
        'Дата закрытия': 'CLOSE_DATE',
        'Источник': 'SOURCE',
        'unom': 'UNOM',
    }, axis=1, inplace=True)
    work_types = work_types[['WORK_NAME', 'CREATE_DATE', 'CLOSE_DATE', 'SOURCE', 'UNOM']]
    job.meta['stage'] = 60
    job.save_meta()
    # окрываем файл с инцидентами, действем по аналогии с предыдушим, чистим и приводим к единому виду
    work_types3 = pd.read_excel(files.get('3.xlsx'))
    work_types3['SOURCE'] = 'DST'

    work_types3.rename({
        'FACT_DATE_START': 'CREATE_DATE',
        'FACT_DATE_END': 'CLOSE_DATE',
    }, axis=1, inplace=True)
    work_types3 = work_types3[['WORK_NAME', 'CREATE_DATE', 'CLOSE_DATE', 'SOURCE', 'UNOM']]
    work_types3['CREATE_DATE'] = (work_types3['CREATE_DATE'].apply(lambda x: reverse_date(x)))
    work_types3['CLOSE_DATE'] = (work_types3['CLOSE_DATE'].apply(lambda x: reverse_date(x)))
    # объединяем все инциденты
    work_types = pd.concat([work_types, work_types3])
    job.meta['stage'] = 70
    job.save_meta()
    # приводим все описания инцидентов в lowercase и смотрим какие уникальные
    work_types['WORK_NAME'] = work_types['WORK_NAME'].str.lower()
    work_types['WORK_NAME'].unique()
    work_types['WORK_CLASS'] = (work_types['WORK_NAME']
                                .apply(lambda x: check_in_type(x, alpabet)))
    pd.DataFrame.iteritems = pd.DataFrame.items
    # преобразуем в числа
    work_types = MultiColumnLabelEncoder(columns=['WORK_CLASS']).fit_transform(work_types)
    # чистим инциденты
    work_types = work_types[work_types['WORK_NAME'].notna()]
    # по хорошему преобразовать дату к числу (int - timestamp) и отсортировать
    work_types = MultiColumnLabelEncoder(columns=[
        'WORK_NAME', 'CREATE_DATE', 'CLOSE_DATE',
        'SOURCE',
    ]).fit_transform(work_types)
    job.meta['stage'] = 80
    job.save_meta()
    # Навсякий случай приводим к int
    df['UNOM'] = df['UNOM'].astype(int)
    work_types['UNOM'] = work_types['UNOM'].astype(int)
    # объединяем с таблицей объектов
    big_df = df.merge(work_types, on='UNOM', how='left')
    # снова чистим, если нет класса
    big_df = big_df[big_df['WORK_CLASS'].notna()]
    big_df = MultiColumnLabelEncoder(columns=['COL_756', 'COL_769']).fit_transform(big_df)
    big_df['ID'] = big_df['ID'].astype(int)
    builds = big_df['NAME'].unique().tolist()
    sum_df = pd.DataFrame()
    job.meta['stage'] = 90
    job.save_meta()
    builds_df = None
    for build in builds:
        builds_df = big_df[big_df['NAME'] == build].sort_values(by='CREATE_DATE')
        builds_df = builds_df.reset_index()
        last = 0
        for i, row in builds_df.iterrows():
            if i == 0:
                last = builds_df.at[i, 'UNOM']
                continue
            last += builds_df.at[i, 'UNOM']
            builds_df.at[i, 'UNOM'] += last
        sum_df = pd.concat([sum_df, builds_df])

    for_model = sum_df.drop(['NAME', 'ID', 'index'], axis=1)
    # for_model.iloc[1000:].to_csv('for_model.csv', sep=',', index=False)
    # for_model.iloc[:1000].to_csv('for_test.csv', sep=',', index=False)
    # sum_df = sum_df[sum_df['UNOM']]
    for_predict = (sum_df.groupby("ID", as_index=False, group_keys=False).apply(lambda x: x.nlargest(1, "UNOM")))
    for_predict.drop(['index', 'WORK_CLASS'], axis=1).to_csv('for_predict_without_unom.csv', sep=',', index=False)

    print(df)
    from sqlalchemy import create_engine
    # sync_db = create_engine(f'postgresql://username:password@localhost:5432/postgres')
    sync_db = create_engine(DB_URL)
    for_model.iloc[1000:].to_sql(name='for_model', con=sync_db, if_exists='replace', index=False)
    for_model.iloc[:1000].to_sql(name='for_test', con=sync_db, if_exists='replace', index=False)
    job.meta['stage'] = 100
    job.save_meta()
    # except Exception as e:
    #     print(e.__str__())
    #     job.meta['stage'] = 0
    #     job.meta['error'] = e.__str__()
    #     job.save_meta()
    # # сохраняем для обучения
    # big_df.to_csv('/Users/sergeyesenin/PycharmProjects/hakaton2/backend/services/upload_data/src/servicedata_for_model2.csv', sep=',', index=False)
    # # сохраняем для предикта
    # big_df.to_csv('/Users/sergeyesenin/PycharmProjects/hakaton2/backend/services/upload_data/src/servicedata_for_model2.csv', sep=',', index=False)


def drop_weather_data(session: Session):
    session.execute(sa_text(f"truncate table {ObjConsumerWeather.__tablename__}"))
    # session.commit()


if __name__ == '__main__':
    files = {}
    prepare_dataset()
