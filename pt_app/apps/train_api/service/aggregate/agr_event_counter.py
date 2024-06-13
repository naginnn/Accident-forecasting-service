from sqlalchemy import text as sa_text
from sqlalchemy.orm import Session
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def agr_events_counters(db, session: Session):
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

    for i, c in consumers.iterrows():
        all_df = pd.DataFrame()
        event_counter_consumer = event_counters[event_counters['obj_consumer_id'] == c['id']]
        events = event_consumers[event_consumers['obj_consumer_id'] == c['id']]
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
        all_df.to_sql(name="counter_consumer_events", schema='public', con=db, if_exists='append', index=False)
