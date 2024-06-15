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
                    ecf.is_closed  as "Статус инцидента",
                    ecf.days_of_work  as "Кол-во дней устранения инцидента"
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
    df_objects["Дата создания инцидента"] = df_objects["Дата создания инцидента"].astype(str)

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")

    df_objects.to_excel(writer, sheet_name="Информация о потребителях", index=False)
    set_column_size(writer, df_objects, "Информация о потребителях")

    writer.close()
    excel_file = output.getvalue()
    return file_name, excel_file


async def create_consumer_station_report(id: int):
    file_name = str(datetime.now().__format__('%d%m%Y')) + '_' + 'consume_station_report'
    consumer_station_query = f"""
                select ocs.name                as "Номер ТП",
                       ld.name as "Округ",
                       la.name as "Район",
                       ocs.address             as "Адрес ТП",
                       ocs.type                as "Вид ТП",
                       ocs.place_type          as "Тип размещения",
                       ocs.ods_name            as "Номер ОДС",
                       ocs.ods_address         as "Адрес ОДС",
                       ocs.ods_manager_company as "Потребитель(или УК)",
                       oss.name                as "Источник теплоснабжения",
                       oss.address             as "Адрес источника",
                       oss.e_power             as "Электро энергия",
                       oss.t_power             as "Тепловая энергия",
                       oss.boiler_count        as "Кол-во котлов",
                       oss.turbine_count       as "Кол-во Турбин"
                from obj_consumer_stations ocs
                         join obj_source_stations oss on oss.id = ocs.id
                         join location_districts ld on ld.id = ocs.location_district_id
                         join location_areas la on la.id = ocs.location_area_id
                where ocs.id = '{str(id)}'
                """
    df_consumer_station = pd.read_sql(consumer_station_query, sync_db)

    objects_query = f"""
                select obj.address        as "Адрес потребителя",
                       ld.name as "Округ",
                       la.name as "Район",
                       obj.total_area     as "Общ. площадь",
                       obj.operating_mode as "Режим работы потребителя",
                       obj.balance_holder as "Балансодержатель",
                       obj.type           as "Тип",
                       obj.priority       as "Приоритет",
                       obj.energy_class   as "Класс энергоэффективности",
                       obj.load_gvs       as "Тепловая нагрузка ГВС ср.",
                       obj.load_fact      as "Тепловая нагрузка ГВС факт.",
                       obj.heat_load      as "Тепловая нагрузка отопления строения",
                       obj.vent_load      as "Тепловая нагрузка вентиляции строения",
                       obj.total_area     as "Общая площадь",
                       obj.build_year     as "Год постройки",
                       obj.wear_pct       as "Фактический износ здания, проц."
                from obj_consumer_stations ocs
                    join obj_consumers obj on ocs.id = obj.obj_consumer_station_id
                    join location_districts ld on ld.id = ocs.location_district_id
                    join location_areas la on la.id = ocs.location_area_id
                where ocs.id = '{str(id)}'
    """
    df_objects = pd.read_sql(objects_query, sync_db)

    events_query = f"""
                        select obj.address        as "Адрес потребителя",
                               ec.description    as "Описание инцидента",
                               ec.created        as "Дата создания инцидента",
                               ec.is_closed      as "Статус инцидента",
                               ec.days_of_work   as "Кол-во дней устранения инцидента",
                               ec.probability    as "Вероятность предсказания",
                               ocs.name           as "Имя ЦТП",
                               ocs.address        as "Адрес ЦТП",
                               ec.source         as "Источник",
                               obj.total_area     as "Общ. площадь",
                               obj.energy_class   as "Класс энергоэффективности",
                               obj.operating_mode as "Режим работы потребителя",
                               obj.priority       as "Приоритет",
                               obj.load_gvs       as "Тепловая нагрузка ГВС ср.",
                               obj.load_fact      as "Тепловая нагрузка ГВС факт.",
                               obj.heat_load      as "Тепловая нагрузка отопления строения",
                               obj.vent_load      as "Тепловая нагрузка вентиляции строения",
                               obj.build_year     as "Год постройки",
                               obj.wear_pct       as "Фактический износ здания, проц."
                        from obj_consumer_stations ocs
                            join obj_consumers obj on ocs.id = obj.obj_consumer_station_id
                            join event_consumers ec on ec.obj_consumer_id = obj.id
                        where ec.is_closed = false and ocs.id = '{str(id)}'
        """
    df_events = pd.read_sql(events_query, sync_db)
    df_events["Дата создания инцидента"] = df_events["Дата создания инцидента"].astype(str)

    event_counter_query = f"""
                select obj.address            as "Адрес потребителя",
                       ec.contour             as "Контур",
                       ec.counter_mark        as "Марка счетчика",
                       ec.counter_number      as "Номер счетчика",
                       ec.gcal_in_system      as "Объем поданного теплоносителя в систему ЦО",
                       ec.gcal_out_system     as "Объем обратного теплоносителя в систему ЦО",
                       ec.subset              as "Разница между подачей и обраткой(Подмес)",
                       ec.leak                as "Разница между подачей и обраткой(Утечка)",
                       ec.supply_temp         as "Температура подачи",
                       ec.return_temp         as "Температура обратки",
                       ec.work_hours_counter  as "Наработка часов счетчика",
                       ec.heat_thermal_energy as "Расход тепловой энергии",
                       ec.errors              as "Ошибка",
                       ec.errors_desc         as "Описание ошибки",
                       ec.created             as "Дата создания",
                       obj.balance_holder     as "Балансодержатель",
                       obj.type               as "Тип",
                       obj.priority           as "Приоритет",
                       obj.energy_class       as "Класс энергоэффективности",
                       obj.build_year         as "Год постройки",
                       obj.wear_pct           as "Фактический износ здания, проц."
                from obj_consumer_stations ocs
                         join obj_consumers obj on ocs.id = obj.obj_consumer_station_id
                         join event_counters ec on ec.obj_consumer_id = obj.id
                where ocs.id = '{str(id)}'
                """
    df_events_counter = pd.read_sql(event_counter_query, sync_db)
    df_events_counter["Дата создания"] = df_events_counter["Дата создания"].astype(str)

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")

    df_consumer_station.to_excel(writer, sheet_name="Информация о ЦТП", index=False)
    df_objects.to_excel(writer, sheet_name="Взаимосвязанные потребители", index=False)
    df_events.to_excel(writer, sheet_name="Открытые инциденты", index=False)
    df_events_counter.to_excel(writer, sheet_name="Выгрузка ОДПУ отопления", index=False)

    set_column_size(writer, df_consumer_station, "Информация о ЦТП")
    set_column_size(writer, df_objects, "Взаимосвязанные потребители")
    set_column_size(writer, df_events, "Открытые инциденты")
    set_column_size(writer, df_events_counter, "Выгрузка ОДПУ отопления")

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
                        ecf.is_closed  as "Статус инцидента",
                        ecf.days_of_work  as "Кол-во дней устранения инцидента",
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
                                      ec.obj_consumer_id,
                                      ec.is_closed,
                                      ec.days_of_work
                               from event_consumers ec
                                        join obj_consumers obj on ec.obj_consumer_id = obj.id) ecf on ecf.obj_consumer_id = obj.id
                         join obj_consumer_stations ocs on obj.obj_consumer_station_id = ocs.id
                    where obj.id = '{str(id)}'
    """
    df_events = pd.read_sql(events_query, sync_db)

    def change_event_status(data):
        if data:
            return "Закрыт"
        elif data is None:
            return '-'
        elif not data:
            return "Открыт"

    df_events["Статус инцидента"] = df_events["Статус инцидента"].apply(lambda x: change_event_status(x))
    df_events["Дата создания инцидента"] = df_events["Дата создания инцидента"].astype(str)

    event_counter_query = f"""
                select obj.address            as "Адрес потребителя",
                       ec.contour             as "Контур",
                       ec.counter_mark        as "Марка счетчика",
                       ec.counter_number      as "Номер счетчика",
                       ec.gcal_in_system      as "Объем поданного теплоносителя в систему ЦО",
                       ec.gcal_out_system     as "Объем обратного теплоносителя в систему ЦО",
                       ec.subset              as "Разница между подачей и обраткой(Подмес)",
                       ec.leak                as "Разница между подачей и обраткой(Утечка)",
                       ec.supply_temp         as "Температура подачи",
                       ec.return_temp         as "Температура обратки",
                       ec.work_hours_counter  as "Наработка часов счетчика",
                       ec.heat_thermal_energy as "Расход тепловой энергии",
                       ec.errors              as "Ошибка",
                       ec.errors_desc         as "Описание ошибки",
                       ec.created             as "Дата создания",
                       obj.balance_holder     as "Балансодержатель",
                       obj.type               as "Тип",
                       obj.priority           as "Приоритет",
                       obj.energy_class       as "Класс энергоэффективности",
                       obj.build_year         as "Год постройки",
                       obj.wear_pct           as "Фактический износ здания, проц."
                from obj_consumers obj
                         join event_counters ec on ec.obj_consumer_id = obj.id
                where obj.id = '{str(id)}'
                """
    df_events_counter = pd.read_sql(event_counter_query, sync_db)
    df_events_counter["Дата создания"] = df_events_counter["Дата создания"].astype(str)

    objects_query = f"""
                select 
                    obj.address as "Адрес потребителя",
                    obj.total_area as "Общ. площадь", 
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
    df_events.to_excel(writer, sheet_name="Инциденты", index=False)
    df_events_counter.to_excel(writer, sheet_name="Выгрузка ОДПУ отопления", index=False)
    df_objects.to_excel(writer, sheet_name="Взаимосвязанные потребители", index=False)

    set_column_size(writer, df_object, "Потребители")
    set_column_size(writer, df_events, "Инциденты")
    set_column_size(writer, df_events_counter, "Выгрузка ОДПУ отопления")
    set_column_size(writer, df_objects, "Взаимосвязанные потребители")

    writer.close()
    excel_file = output.getvalue()
    return file_name, excel_file


# if __name__ == '__main__':
#     # asyncio.run(create_objects_report())
#     # asyncio.run(create_object_report(5))
#     asyncio.run(create_consumer_station_report(1))
