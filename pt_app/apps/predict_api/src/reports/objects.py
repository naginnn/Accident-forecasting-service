import asyncio
import io

import pandas as pd
from datetime import datetime
from settings.db import sync_db


async def create_objects_report():
    file_name = str(datetime.now().__format__('%d%m%Y')) + '_' + 'objects_report'
    query = """
                select 
                    obj.address        as "Адрес потребителя",
                    ld.name            as "Округ",
                    la.name            as "Район",
                    obj.operating_mode as "Режим работы потребителя",
                    ss.name            as "Имя источника",
                    ss.address         as "Адрес источника",
                    ocs.name           as "Имя ЦТП",
                    ocs.address        as "Адрес ЦТП",
                    ecf.probability    as "Вероятность предсказания, %"
                from obj_source_stations ss
                    join obj_consumer_stations ocs on ss.location_area_id = ocs.location_area_id
                    join obj_consumers obj on obj.obj_consumer_station_id = ss.id
                    join location_districts ld on obj.location_district_id = ld.id
                    join location_areas la on obj.location_area_id = la.id
                    left join (
                        select ecc.obj_consumer_id, max(ecc.id) as id
                        from event_consumers as ecc
                        group by obj_consumer_id) ec on ec.obj_consumer_id = ocs.id
                    left join event_consumers ecf on ecf.id = ec.id
                """
    df_objects = pd.read_sql(query, sync_db)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")

    def set_column_size(df, sheet_name, **kwargs):
        writer.sheets[sheet_name].autofilter(0, 0, df.shape[1], df.shape[1])
        for column in df:
            if kwargs.get("unique_columns", {}).get(column):
                column_width = kwargs.get("unique_columns").get(column)
            else:
                column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet_name].set_column(col_idx, col_idx, column_width)

    df_objects.to_excel(writer, sheet_name="Информация о потребителях", index=False)
    set_column_size(df_objects, "Информация о потребителях")

    writer.close()
    excel_file = output.getvalue()
    return file_name, excel_file


async def create_object_report(id: int):
    file_name = str(datetime.now().__format__('%d%m%Y')) + '_' + 'object_report'
    obj_query = f"""
                select
                    ld.name as "Округ", la.name as "Район",
                    obj.address as "Адрес потребителя", 
                    obj.operating_mode as "Режим работы потребителя",
                    ocs.name as "Имя ЦТП", ocs.address as "Адрес ЦТП"
                from obj_consumers obj
                join location_districts ld on obj.location_district_id = ld.id
                join location_areas la on obj.location_area_id = la.id
                join obj_consumer_stations ocs on obj.obj_consumer_station_id = ocs.id
                where obj.id = '{str(id)}'
                """
    df_object = pd.read_sql(obj_query, sync_db)

    events_query = f"""
                    select
                        obj.address        as "Адрес потребителя",
                        obj.total_area     as "Общ. площадь",
                        obj.energy_class   as "Класс энергоэффективности",
                        obj.operating_mode as "Режим работы потребителя",
                        obj.priority       as "Приоритет",
                        ocs.name           as "Имя ЦТП",
                        ocs.address        as "Адрес ЦТП",
                        ecf.source         as "Источник",
                        ecf.description    as "Описание",
                        ecf.created        as "Дата создания",
                        ecf.probability    as "Вероятность предсказания, %"
                    from obj_consumers obj
                         join (select ec.source,
                                      ec.description,
                                      ec.created,
                                      ec.probability,
                                      ec.obj_consumer_id
                               from event_consumers ec
                                        join obj_consumers obj on ec.obj_consumer_id = obj.id
                               where ec.is_closed = false) ecf on ecf.obj_consumer_id = obj.id
                         join obj_consumer_stations ocs on obj.obj_consumer_station_id = ocs.id
                    where obj.id = '{str(id)}'
    """
    df_events = pd.read_sql(events_query, sync_db)

    objects_query = f"""
                select 
                    obj.address as "Адрес потребителя",
                    obj.total_area as "Общ. площадь", 
                    obj.energy_class as "Класс энергоэффективности", 
                    obj.operating_mode as "Режим работы потребителя",
                    obj.priority as "Приоритет"
                from obj_consumers obj
                where obj.obj_consumer_station_id = (
                        select ocs.id
                        from obj_consumers obj
                        join obj_consumer_stations ocs on obj.obj_consumer_station_id = ocs.id
                where obj.id = '{str(id)}')
    """
    df_objects = pd.read_sql(objects_query, sync_db)

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")

    def set_column_size(df, sheet_name, **kwargs):
        writer.sheets[sheet_name].autofilter(0, 0, df.shape[1], df.shape[1])
        for column in df:
            if kwargs.get("unique_columns", {}).get(column):
                column_width = kwargs.get("unique_columns").get(column)
            else:
                column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet_name].set_column(col_idx, col_idx, column_width)

    df_object.to_excel(writer, sheet_name="Информация о потребителе", index=False)
    df_events.to_excel(writer, sheet_name="Открытые инциденты", index=False)
    df_objects.to_excel(writer, sheet_name="Взаимосвязанные потребители", index=False)
    set_column_size(df_object, "Информация о потребителе")
    set_column_size(df_events, "Открытые инциденты")
    set_column_size(df_objects, "Взаимосвязанные потребители")

    writer.close()
    excel_file = output.getvalue()
    return file_name, excel_file


if __name__ == '__main__':
    asyncio.run(create_object_report(7))
