import asyncio
import os
import threading
import time

import pandas as pd
from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Connection, create_engine, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from apps.train_api.service.agregate import agr_for_view, agr_for_train, agr_for_unprocessed, upload
from apps.train_api.service.receive import (collect_data, predict_data, save_unprocessed_data,
                                            get_unprocessed_data, get_processed_data)

from settings.rd import get_redis_client


class Data:
    data: pd.DataFrame


def load_data(event_counter_consumer, events, all_df):
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


if __name__ == '__main__':
    start = time.time()
    PG_USR = os.getenv('POSTGRES_USER', 'username')
    PG_PWD = os.getenv('POSTGRES_PASSWORD', 'password')
    PG_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    PG_PORT = os.getenv('POSTGRES_PORT', '5432')
    PG_DB_NAME = os.getenv('POSTGRES_DB', 'postgres')
    db = create_engine(f'postgresql://{PG_USR}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}')
    query = sa_text(
        """
        with ids as (select -- связываем id (потребителя, события, счеткика, предыдущего события)
 oc.id cons_id,
 ec.id event_id,
 ec2.id counter_id,
 (
  select ec3.id
   from event_consumers ec3
   where oc.id = ec3.obj_consumer_id and ec3.created < ec.created
   order by ec3.created desc
   limit 1
 ) prev_event_id
 from obj_consumers oc
 left join event_consumers ec on oc.id = ec.obj_consumer_id
 left join event_counters ec2 on oc.id = ec2.obj_consumer_id where oc.id = 2
                                     and ec2.created >= ec.created and ec2.created <= ec.closed
 order by oc.id, ec.created
)
select
--     oc.*,
--     ec.*,
    ec.id, ec.obj_consumer_id, ec.description, ec.days_of_work,
    ec.created event_created, ec.closed event_closed,
--     ec2.*,
    ec2.id, ec2.obj_consumer_id, ec2.created counter_event_created,
            ec2.gcal_in_system, ec2.gcal_out_system, ec2.subset, ec2.leak,
            ec2.supply_temp, ec2.return_temp, ec2.heat_thermal_energy,
            ec2.errors, ec2.errors_desc
--     ec3.*
from ids -- выбираем нужную инфу, связывая нужные таблицы по id из таблицы ids
left join obj_consumers oc on oc.id = ids.cons_id
left join event_consumers ec on ec.id = ids.event_id
left join event_counters ec2 on ec2.id = ids.counter_id
-- left join event_consumers ec3 on ec3.id = ids.prev_event_id
        """
    )
    df = pd.read_sql(query, db)


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


    all_df = pd.DataFrame()
    for i, c in consumers.iterrows():
        tmp_df = pd.DataFrame()
        event_counter_consumer = event_counters[event_counters['obj_consumer_id'] == c['id']]
        events = event_consumers[event_consumers['obj_consumer_id'] == c['id']]
        # event_counter_consumer = event_counters[event_counters['obj_consumer_id'] == 2]
        # events = event_consumers[event_consumers['obj_consumer_id'] == 2]
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
        print('Прогнали', all_df.shape)


    all_df.to_excel('lala.xlsx')
    print(time.time() - start)



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

# threads = []
# for filename in os.listdir("../../../autostart"):
#     thread = threading.Thread(target=load_data, args=(files, filename,), daemon=True)
#     threads.append(thread)
#     thread.start()
# for thread in threads:
#     thread.join()

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
