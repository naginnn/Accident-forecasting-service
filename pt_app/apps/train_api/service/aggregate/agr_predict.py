# from sqlalchemy import Engine, text as sa_text
# import pandas as pd
#
# from settings.db import sync_db
#
#
# class AgrPredict:
#     def __init__(self, db: Engine, obj_consumer_ids: list[int]):
#         self.db = db
#         self.obj_consumer_ids = obj_consumer_ids
#         self.__get_data_from_db()
#
#     def __get_data_from_db(self):
#         consumer_ids = ",".join([str(i) for i in self.obj_consumer_ids])
#         query = sa_text(
#             f"""
#                             select * from postgres.public.obj_consumers where id in ({consumer_ids})
#                             """
#         )
#         consumers = pd.read_sql(query, self.db)
#         query = sa_text(
#             f"""
#                         select ec.id, ec.obj_consumer_id, ec.description, ec.days_of_work,
#                          ec.created event_created, ec.closed event_closed
#                         from postgres.public.event_consumers ec
#                         where ec.is_closed = true
#                         and ec.obj_consumer_id in ({consumer_ids})
#                         order by created
#                         """
#         )
#         event_consumers = pd.read_sql(query, self.db).reset_index()
#         query = sa_text(
#             f"""
#                             select
#                             ec.id, ec.obj_consumer_id, ec.created counter_event_created,
#                             ec.gcal_in_system, ec.gcal_out_system, ec.subset, ec.leak,
#                             ec.supply_temp, ec.return_temp, ec.heat_thermal_energy,
#                             ec.errors, ec.errors_desc
#                             from postgres.public.event_counters ec
#                             where ec.obj_consumer_id in ({consumer_ids})
#                             order by created
#                             """
#         )
#         event_counters = pd.read_sql(query, self.db).reset_index()
#         print('start')
#
#         def res(x, storage):
#             event_counter_consumer = event_counters[event_counters['obj_consumer_id'] == x]
#             events = event_consumers[event_consumers['obj_consumer_id'] == x]
#             if event_counter_consumer.empty and events.empty:
#                 return
#             all_df = pd.DataFrame()
#             used_events = []
#             for j, ecc in event_counter_consumer.iterrows():
#                 between = events[
#                     (ecc['counter_event_created'] >= events['event_created']) & (
#                             ecc['counter_event_created'] <= events['event_closed'])
#                     ]
#                 used_events += between['id'].tolist()
#                 lala = pd.DataFrame([ecc])
#                 lala.drop('index', inplace=True, axis=1)
#                 tmp_df = pd.merge(lala, between, how='left', on='obj_consumer_id')
#                 all_df = pd.concat([all_df, tmp_df])
#             if used_events:
#                 events = events[~events['id'].isin(used_events)]
#             if not all_df.empty:
#                 all_df = pd.concat([all_df, events])
#                 storage.append(all_df)
#
#         storage = []
#         consumers['id'].apply(lambda x: res(x, storage))
#         events_all = pd.DataFrame()
#         for st in storage:
#             events_all = pd.concat([events_all, st])
#         return events_all
#
#     def agr_for_predict(self):
#         counter_consumer_events = self.__get_data_from_db()
#
#
#
# if __name__ == '__main__':
#     cc = ",".join([str(i) for i in [1, 2, 3]])
#     AgrPredict(db=sync_db, obj_consumer_ids=[1, 2, 3])
