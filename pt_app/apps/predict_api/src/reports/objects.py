import asyncio
import io

import pandas as pd
from datetime import datetime
from settings.db import sync_db


def set_column_size(writer, df, sheet_name, **kwargs):
    writer.sheets[sheet_name].autofilter(0, 0, df.shape[1], df.shape[1])
    for column in df:
        if kwargs.get("unique_columns", {}).get(column):
            column_width = kwargs.get("unique_columns").get(column)
        else:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets[sheet_name].set_column(col_idx, col_idx, column_width)


async def create_objects_report():
    file_name = str(datetime.now().__format__('%d%m%Y')) + '_' + 'objects_report'
    query = """
                select
                    c.address as "Адрес потребителя", 
                    ld.name as "Округ",
                    la.name as "Район",
                    ss.name as "Источник", 
                    ss.address as "Адрес источника", 
                    cs.name as "Имя ЦТП", 
                    cs.address as "Адрес ЦТП",
                    c.balance_holder as "Балансодержатель",
                    c.operating_mode as "Режим работы потребителя",
                    c.type as "Тип",
                    c.total_area as "Общая площадь",
                    c.build_year as "Год постройки",
                    c.wear_pct as "Фактический износ здания, проц.",
                    c.priority as "Приоритет",
                    c.energy_class as "Класс энергоэффективности",
                    c.load_gvs as "Тепловая нагрузка ГВС ср.",
                    c.load_fact as "Тепловая нагрузка ГВС факт.",
                    c.heat_load as "Тепловая нагрузка отопления строения",
                    c.vent_load as "Тепловая нагрузка вентиляции строения",
                    ecf.probability  as "Вероятность предсказания",
                    ecf.description  as "Последний инцидент",
                    ecf.created  as "Дата создания инцидента",
                    ecf.is_closed  as "Статус инцидента"
                from obj_consumers as c
                         join public.location_districts ld on ld.id = c.location_district_id
                         join public.location_areas la on la.id = c.location_area_id
                         join public.obj_consumer_stations cs on cs.id = c.obj_consumer_station_id
                         join public.obj_source_consumer_stations scs on cs.id = scs.obj_consumer_station_id
                         join public.obj_source_stations ss on ss.id = scs.obj_source_station_id
                         left join (select ecc.obj_consumer_id, max(ecc.id) as id from public.event_consumers as ecc group by obj_consumer_id) ec on ec.obj_consumer_id = cs.id
                         left join public.event_consumers ecf on ecf.id = ec.id
                """
    df_objects = pd.read_sql(query, sync_db)

    def change_event_status(data):
        if data:
            return "Открыт"
        elif data is None:
            return '-'
        elif not data:
            return "Закрыт"

    df_objects["Статус инцидента"] = df_objects["Статус инцидента"].apply(lambda x: change_event_status(x))
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")

    df_objects.to_excel(writer, sheet_name="Информация о потребителях", index=False)
    set_column_size(writer, df_objects, "Информация о потребителях")

    writer.close()
    excel_file = output.getvalue()
    return file_name, excel_file


async def create_object_report(id: int):
    file_name = str(datetime.now().__format__('%d%m%Y')) + '_' + 'object_report'
    obj_query = f"""
                select
                    obj.address as "Адрес потребителя", 
                    ld.name as "Округ", 
                    la.name as "Район",
                    obj.address as "Адрес потребителя", 
                    ocs.name as "Имя ЦТП", 
                    ocs.address as "Адрес ЦТП",
                    obj.balance_holder as "Балансодержатель",
                    obj.operating_mode as "Режим работы потребителя",
                    obj.type as "Тип",
                    obj.total_area as "Общая площадь",
                    obj.build_year as "Год постройки",
                    obj.wear_pct as "Фактический износ здания, проц.",
                    obj.priority as "Приоритет",
                    obj.energy_class as "Класс энергоэффективности",
                    obj.load_gvs as "Тепловая нагрузка ГВС ср.",
                    obj.load_fact as "Тепловая нагрузка ГВС факт.",
                    obj.heat_load as "Тепловая нагрузка отопления строения",
                    obj.vent_load as "Тепловая нагрузка вентиляции строения"
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
                        ecf.description    as "Описание инцидента",
                        ecf.created        as "Дата создания инцидента",
                        ecf.probability    as "Вероятность предсказания",
                        ocs.name           as "Имя ЦТП",
                        ocs.address        as "Адрес ЦТП",
                        ecf.source         as "Источник",
                        obj.total_area     as "Общ. площадь",
                        obj.energy_class   as "Класс энергоэффективности",
                        obj.operating_mode as "Режим работы потребителя",
                        obj.priority       as "Приоритет",
                        obj.load_gvs as "Тепловая нагрузка ГВС ср.",
                        obj.load_fact as "Тепловая нагрузка ГВС факт.",
                        obj.heat_load as "Тепловая нагрузка отопления строения",
                        obj.vent_load as "Тепловая нагрузка вентиляции строения",
                        obj.build_year as "Год постройки",
                        obj.wear_pct as "Фактический износ здания, проц."
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
                    obj.balance_holder as "Балансодержатель",
                    obj.type as "Тип",
                    obj.priority as "Приоритет",
                    obj.energy_class as "Класс энергоэффективности",
                    obj.load_gvs as "Тепловая нагрузка ГВС ср.",
                    obj.load_fact as "Тепловая нагрузка ГВС факт.",
                    obj.heat_load as "Тепловая нагрузка отопления строения",
                    obj.vent_load as "Тепловая нагрузка вентиляции строения",
                    obj.total_area as "Общая площадь",
                    obj.build_year as "Год постройки",
                    obj.wear_pct as "Фактический износ здания, проц."
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

    df_object.to_excel(writer, sheet_name="Потребители", index=False)
    df_events.to_excel(writer, sheet_name="Открытые инциденты", index=False)
    df_objects.to_excel(writer, sheet_name="Взаимосвязанные потребители", index=False)
    set_column_size(writer, df_object, "Потребители")
    set_column_size(writer, df_events, "Открытые инциденты")
    set_column_size(writer, df_objects, "Взаимосвязанные потребители")

    writer.close()
    excel_file = output.getvalue()
    return file_name, excel_file


if __name__ == '__main__':
    # asyncio.run(create_objects_report())
    asyncio.run(create_object_report(10))
