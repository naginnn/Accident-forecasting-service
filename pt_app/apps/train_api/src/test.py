import asyncio
import os
import threading
import time

import pandas as pd
# import modin.pandas as pd
from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Connection, create_engine, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from apps.train_api.service.agregate import agr_for_view, agr_for_train, agr_for_unprocessed, upload
from apps.train_api.service.receive import (collect_data, predict_data, save_unprocessed_data,
                                            get_unprocessed_data, get_processed_data)

from settings.rd import get_redis_client
from concurrent.futures import ThreadPoolExecutor


def load_data(name, event_counter_consumer, events, saver, db):

    all_df = pd.DataFrame()
    tmp_df = pd.DataFrame()
    used_events = []

    for j, ecc in event_counter_consumer.iterrows():
        between = events[
            (ecc['counter_event_created'] >= events['event_created']) & (
                    ecc['counter_event_created'] <= events['event_closed'])
            ]
        used_events += between['id'].tolist()
        lala = pd.DataFrame([ecc])
        lala.drop('index', inplace=True, axis=1)
        tmp_df = pd.merge(lala, between, how='left', on='obj_consumer_id')
        all_df = pd.concat([all_df, tmp_df])

    if used_events:
        events = events[~events['id'].isin(used_events)]
    all_df = pd.concat([all_df, events])
    all_df.to_sql(name="lala", con=db, if_exists='append', index=False)
    print('Прогнали', all_df.shape)
    # saver['all_df'] = pd.concat([saver['all_df'], all_df])
    # print(saver['all_df'].shape[0])



if __name__ == '__main__':
    start = time.time()
    PG_USR = os.getenv('POSTGRES_USER', 'username')
    PG_PWD = os.getenv('POSTGRES_PASSWORD', 'password')
    PG_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    PG_PORT = os.getenv('POSTGRES_PORT', '5432')
    PG_DB_NAME = os.getenv('POSTGRES_DB', 'postgres')
    db = create_engine(f'postgresql://{PG_USR}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}')

    query = sa_text(
        f"""
            select * from postgres.public.obj_consumers
            """
    )
    consumers = pd.read_sql(query, db)
    query = sa_text(
        f"""
        select ec.id, ec.obj_consumer_id, ec.description, ec.days_of_work,
         ec.created event_created, ec.closed event_closed
        from postgres.public.event_consumers ec 
        where ec.is_closed = true 
--         and ec.obj_consumer_id = 2 
        order by created
        """
    )
    event_consumers = pd.read_sql(query, db).reset_index()
    query = sa_text(
        f"""
            select 
            ec.id, ec.obj_consumer_id, ec.created counter_event_created,
            ec.gcal_in_system, ec.gcal_out_system, ec.subset, ec.leak,
            ec.supply_temp, ec.return_temp, ec.heat_thermal_energy,
            ec.errors, ec.errors_desc
            from postgres.public.event_counters ec 
--             where ec.obj_consumer_id = 2  
            order by created
            """
    )
    event_counters = pd.read_sql(query, db).reset_index()

    # all_df = pd.DataFrame()
    # for i, c in consumers.iterrows():
    #     tmp_df = pd.DataFrame()
    #     event_counter_consumer = event_counters[event_counters['obj_consumer_id'] == c['id']]
    #     events = event_consumers[event_consumers['obj_consumer_id'] == c['id']]
    #     # event_counter_consumer = event_counters[event_counters['obj_consumer_id'] == 2]
    #     # events = event_consumers[event_consumers['obj_consumer_id'] == 2]
    #     used_events = []
    #     for j, ecc in event_counter_consumer.iterrows():
    #         between = events[
    #             (ecc['counter_event_created'] >= events['event_created']) & (
    #                         ecc['counter_event_created'] <= events['event_closed'])
    #             ]
    #         used_events += between['id'].tolist()
    #         lala = pd.DataFrame([ecc])
    #         lala.drop('index', inplace=True, axis=1)
    #         tmp_df = pd.merge(lala, between, how='left', on='obj_consumer_id')
    #         all_df = pd.concat([all_df, tmp_df])
    #
    #     if used_events:
    #         events = events[~events['id'].isin(used_events)]
    #     all_df = pd.concat([all_df, events])
    #     print('Прогнали', all_df.shape)
    #
    #
    # all_df.to_excel('lala.xlsx')
    # print(time.time() - start)

    # threads = []
    # all_df = pd.DataFrame()
    # for i, c in consumers.iterrows():
    #     event_counter_consumer = event_counters[event_counters['obj_consumer_id'] == c['id']]
    #     events = event_consumers[event_consumers['obj_consumer_id'] == c['id']]
    #     thread = threading.Thread(target=load_data, args=(event_counter_consumer, events, all_df,), daemon=True)
    #     threads.append(thread)
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    #     print(all_df)
    print('started')
    threads = []
    saver = {'all_df': pd.DataFrame()}
    with ThreadPoolExecutor(max_workers=40) as executor:
        # Создаём список задач
        futures = []
        for i, c in consumers.iterrows():
            tmp_df = pd.DataFrame()
            event_counter_consumer = event_counters[event_counters['obj_consumer_id'] == c['id']]
            events = event_consumers[event_consumers['obj_consumer_id'] == c['id']]
            # event_counter_consumer = event_counters[event_counters['obj_consumer_id'] == 2]
            # events = event_consumers[event_consumers['obj_consumer_id'] == 2]
            future = executor.submit(load_data, i, event_counter_consumer, events, saver, db)
            futures.append(future)
        for future in futures:
            future.result()
        df = saver.get('all_df')
        df.to_excel('data.xlsx')
        print(time.time() - start)

    # df['event_id'] = df['accident']
    # consumers = df['consumer_id'].unique().tolist()
    # df['last_event_id'] = 0
    # # df['between_created'] = 0
    # train_df = pd.DataFrame()
    # last = 0
    # for consumer in consumers:
    #     consumers_df = df[df['consumer_id'] == consumer].sort_values(by='event_created', ascending=True)
    #     consumers_df = consumers_df.reset_index()
    #     for i, row in consumers_df.iterrows():
    #         if i > 0:
    #             last = consumers_df.at[i - 1, 'event_id']
    #             consumers_df.at[i, 'last_event_id'] = last
    #         else:
    #             consumers_df.at[i, 'last_event_id'] = last
    #     consumers_df = consumers_df[(consumers_df['event_id'] != 0) | (consumers_df['last_event_id'] != 0)]
    #     train_df = pd.concat([train_df, consumers_df])
    # print()

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
