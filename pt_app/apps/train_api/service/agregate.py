import datetime
import os
import pickle
import threading
from typing import Tuple
import numpy as np
from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import re
from rq import Queue
from rq.command import send_stop_job_command
from rq.exceptions import *
from rq.job import Job, get_current_job
from apps.train_api.service.utils import MultiColumnLabelEncoder
from settings.rd import get_redis_client

pd.options.mode.chained_assignment = None  # default='warn'


def agr_for_view(tables: dict) -> dict:
    """Агрегация данных"""
    agr_tables = {}
    flat_table = tables.get('flat_table')
    events_all = tables.get('events_all')
    event_types = tables.get('event_types')
    events_counter_all = tables.get('events_counter_all')
    outage = tables.get('outage')
    flat_table = AgrView.update_coordinates(flat_table)
    flat_table = AgrView.clean_types(flat_table)
    flat_table = AgrView.get_operation_mode(flat_table)
    flat_table = AgrView.get_sock(flat_table)
    flat_table = AgrView.get_ranking(flat_table)
    flat_table = AgrView.get_temp_conditions(flat_table)
    # flat_table = AgrView.get_temp_conditions(flat_table)
    # flat_table = AgrView.split_address(flat_table)
    # flat_table = AgrView.split_wall_materials(flat_table, df_wall_materials)
    # df_events = tables.get('test_events_all')
    # df_events = AgrView.get_work_days(df_events)
    events_all = AgrView.filter_events(events_all, event_types)
    events_all = AgrView.get_work_days(events_all)

    events_counter_all['month_year'] = events_counter_all['month_year'].astype('datetime64[ns]')
    agr_tables["flat_table"] = flat_table
    agr_tables["events_all"] = events_all
    agr_tables["events_counter_all"] = events_counter_all
    agr_tables["outage"] = outage
    return agr_tables


def agr_for_train(tables: dict) -> tuple:
    df = tables.get('view_table')
    events_df = tables.get('event_types')
    df = AgrTrain.agr_date(df)
    df = AgrTrain.get_work_class(df, events_df)
    # df = AgrTrain.get_work_classes_all(df)
    # Преобразуем в числовые параметры
    # close time не учитывать при обучении, интервал тоже
    df = AgrTrain.clear_data(df)

    # df = MultiColumnLabelEncoder(columns=[
    #     'consumer_address', 'consumer_name',
    # ]).fit_transform(df)
    agr_train_df = AgrTrain.get_train_data(df)
    agr_predict_df = AgrTrain.get_predict_data(agr_train_df)
    agr_train_df.to_csv("agr_train_df.csv", index=False)
    agr_predict_df.to_csv("agr_predict_df.csv", index=False)
    # agr_train_tables["full"] = tables.get('test_full')
    # agr_predict_tables["full"] = tables.get('test_full')
    return agr_predict_df, agr_train_df


def read_excel(tables: dict, file, sheet_name: str = None):
    df = pd.read_excel(tables[file], sheet_name=sheet_name)
    tables[file] = df


def agr_for_unprocessed(tables: dict) -> dict:
    agr_tables = {}

    main_df = pd.read_excel(tables.get('7.xlsx'))

    bti_df = AgrUnprocessed.agr_bti(pd.read_excel(tables.get('9.xlsx')))
    big_df = main_df.merge(bti_df[[
        'UNOM', 'Адрес строения',
        'Административный округ', 'Муниципальный округ',
        'Улица', 'Тип номера дом', 'Номер дома',
        'Номер корпуса', 'Тип номера строения/сооружения',
        'Номер строения',
        'Материал', 'Назначение', 'Класс', 'Тип', 'Этажность', 'Общая площадь',
        # ]], how="left", on='Адрес строения')
    ]], how="inner", on='Адрес строения')
    tp_df = bti_df.__deepcopy__()
    tp_df.columns = ['id_ТП', 'Город_ТП', 'Административный округ_ТП',
                     'Муниципальный округ_ТП', 'Населенный пункт_ТП',
                     'Улица_ТП', 'Тип номера дом_ТП', 'Номер дома_ТП',
                     'Номер корпуса_ТП', 'Тип номера строения/сооружения_ТП',
                     'Номер строения_ТП', 'UNOM_ТП', 'UNAD_ТП',
                     'Материал_ТП', 'Назначение_ТП', 'Класс_ТП', 'Тип_ТП', 'Этажность_ТП', 'Признак_ТП',
                     'Общая площадь_ТП', 'Адрес строения ТП', 'Адрес ТП'
                     ]
    with_tp_df = big_df.merge(tp_df[['UNOM_ТП', 'Адрес ТП']], how="inner", on='Адрес ТП')

    # threads['13.xlsx'].join()
    df_coord = pd.read_excel(tables.get("13.xlsx"))
    df_coord = df_coord[1:]
    df_coord['UNOM'] = df_coord['UNOM'].astype(float)
    res = with_tp_df.merge(df_coord[['geoData', 'geodata_center', 'UNOM']], how="inner", on='UNOM')
    df_coord = df_coord.rename(
        columns={'UNOM': 'UNOM_ТП', 'geoData': 'geoData_ТП', 'geodata_center': 'geodata_center_ТП'}).__deepcopy__()
    res2 = res.merge(df_coord[['geoData_ТП', 'geodata_center_ТП', 'UNOM_ТП']], how="inner", on='UNOM_ТП')
    res2['geodata_center'] = res2['geodata_center'].apply(lambda x: Utils.get_coord(x))
    res2['geoData'] = res2['geoData'].apply(lambda x: Utils.get_coord(x, darr=True))
    res2['geodata_center_ТП'] = res2['geodata_center_ТП'].apply(lambda x: Utils.get_coord(x))
    res2['geoData_ТП'] = res2['geoData_ТП'].apply(lambda x: Utils.get_coord(x, darr=True))
    res2['Источник теплоснабжения'].unique().tolist()
    res2['geoData_ТЭЦ'] = res2['Источник теплоснабжения'].apply(lambda x: Utils.set_obj_source_station_coord(x))
    res2["Адрес ТЭЦ"] = res2['geoData_ТЭЦ'].apply(lambda x: Utils.get_addr(x))
    res2.rename(columns={
        'Источник теплоснабжения': 'obj_source_name',
        'Дата ввода в эксплуатацию': 'obj_source_launched',
        'Адрес ТЭЦ': 'obj_source_address',
        'geoData_ТЭЦ': 'obj_source_geodata_center',
        # obj_consumer_station
        'Административный округ (ТП)': 'obj_consumer_station_location_district',
        'Муниципальный район': 'obj_consumer_station_location_area',
        'Номер ТП': 'obj_consumer_station_name',
        'Адрес ТП': 'obj_consumer_station_address',
        'Вид ТП': 'obj_consumer_station_type',
        'Тип по размещению': 'obj_consumer_station_place_type',
        'UNOM_ТП': 'obj_consumer_station_unom',
        'geoData_ТП': 'obj_consumer_station_geodata',
        'geodata_center_ТП': 'obj_consumer_station_geodata_center',
        # obj_consumer
        'Адрес строения': 'obj_consumer_address',
        'Балансодержатель': 'obj_consumer_balance_holder',
        'Тепловая нагрузка ГВС ср.': 'obj_consumer_gvs_load_avg',
        'Тепловая нагрузка ГВС факт.': 'obj_consumer_gvs_load_fact',
        'Тепловая нагрузка отопления строения': 'obj_consumer_heat_build_load',
        'Тепловая нагрузка вентиляции строения': 'obj_consumer_vent_build_load',
        'Диспетчеризация': 'obj_consumer_is_dispatch',
        'UNOM': 'obj_consumer_unom',
        'Административный округ': 'obj_consumer_location_district',
        'Муниципальный округ': 'obj_consumer_location_area',
        'Улица': 'obj_consumer_street',
        'Тип номера дом': 'obj_consumer_house_type',
        'Номер дома': 'obj_consumer_house_number',
        'Номер корпуса': 'obj_consumer_corpus_number',
        'Тип номера строения/сооружения': 'obj_consumer_soor_type',
        'Номер строения': 'obj_consumer_soor_number',
        'Материал': 'wall_material',
        'Назначение': 'obj_consumer_target',
        'Класс': 'obj_consumer_class',
        'Тип': 'obj_consumer_build_type',
        'Этажность': 'obj_consumer_build_floors',
        'Общая площадь': 'obj_consumer_total_area',
        'geoData': 'obj_consumer_geodata',
        'geodata_center': 'obj_consumer_geodata_center',
    }, inplace=True)
    obj_source_columns = (
        'obj_source_e_power',
        'obj_source_t_power',
        'obj_source_boiler_count',
        'obj_source_turbine_count'
    )
    res2[[*obj_source_columns]] = res2['obj_source_name'].apply(lambda x: pd.Series(Utils.get_source_data(x)))

    res2 = res2[[
        # source station
        'obj_source_name', 'obj_source_launched', 'obj_source_address',
        'obj_source_e_power',
        'obj_source_t_power',
        'obj_source_boiler_count',
        'obj_source_turbine_count',
        'obj_source_geodata_center',
        # consumer_station
        'obj_consumer_station_location_district', 'obj_consumer_station_location_area', 'obj_consumer_station_name',
        'obj_consumer_station_address', 'obj_consumer_station_type',
        'obj_consumer_station_place_type', 'obj_consumer_station_unom',
        'obj_consumer_station_geodata',
        'obj_consumer_station_geodata_center',
        # obj_consumer
        'obj_consumer_address',
        'obj_consumer_balance_holder',
        'obj_consumer_gvs_load_avg',
        'obj_consumer_gvs_load_fact',
        'obj_consumer_heat_build_load',
        'obj_consumer_vent_build_load',
        'obj_consumer_is_dispatch',
        'obj_consumer_unom',
        'obj_consumer_location_district',
        'obj_consumer_location_area',
        'obj_consumer_street',
        'obj_consumer_house_type',
        'obj_consumer_house_number',
        'obj_consumer_corpus_number',
        'obj_consumer_soor_type',
        'obj_consumer_soor_number',
        'wall_material',
        'obj_consumer_target',
        'obj_consumer_class',
        'obj_consumer_build_type',
        'obj_consumer_build_floors',
        'obj_consumer_total_area',
        'obj_consumer_geodata',
        'obj_consumer_geodata_center',
    ]]
    # threads['8.xlsx'].join()
    ods_df = AgrUnprocessed.agr_ods(pd.read_excel(tables.get('8.xlsx')))
    res2 = res2.merge(ods_df[['obj_consumer_station_name',
                              'obj_consumer_station_ods_name',
                              'obj_consumer_station_ods_address',
                              'obj_consumer_station_ods_id_yy',
                              'obj_consumer_station_ods_manager_company',
                              ]], how='left', on='obj_consumer_station_name')
    res2.fillna("Нет данных", inplace=True)
    # dsadsa
    res2['wall_material_k'] = res2['wall_material'].apply(lambda x: Utils.check_heat_resist(x))
    # threads['5.xlsx'].join()
    # threads['5.1.xlsx'].join()
    events = pd.read_excel(tables.get('5.xlsx'), sheet_name='Выгрузка')
    events2 = pd.read_excel(tables.get('5.1.xlsx'), sheet_name='Выгрузка')
    events2.rename(columns={'Дата и время завершения события': 'Дата и время завершения события во внешней системе'},
                   inplace=True)
    events = pd.concat([events, events2])
    events.rename(columns={
        'Наименование': 'event_description',
        'Источник': 'event_source',
        'Дата создания во внешней системе': 'event_created',
        'Дата закрытия': 'event_closed_ext',
        'Округ': 'location_area',
        'УНОМ': 'unom',
        'Адрес': 'address',
        'Дата и время завершения события во внешней системе': 'event_closed',
    }, inplace=True)

    #
    # events_counter = pd.read_excel(tables.get('11.xlsx'), sheet_name='Sheet 1')
    # events_counter2 = pd.read_excel(tables.get('11.xlsx'), sheet_name='Sheet 2')
    #
    # events_counter_all = pd.concat([events_counter, events_counter2])
    # events_counter_all.rename(columns={
    #     'ID УУ': 'obj_consumer_station_ods_id_yy',
    #     'ID ТУ': 'obj_consumer_station_ods_id_ty',
    #     'Округ': 'district',
    #     'Район': 'area',
    #     'Потребители': 'obj_consumer_station_ods_manager_company',
    #     'Группа': 'group',
    #     'UNOM': 'unom',
    #     'Адрес': 'address',
    #     'Центральное отопление(контур)': 'central_heating',
    #     'Марка счетчика ': 'counter_brand',
    #     'Серия/Номер счетчика': 'number_brand',
    #     'Дата': 'date', 'Месяц/Год': 'month_year', 'Unit': 'unit',
    #     'Температура подачи': 'supply_temperature',
    #     'Объём поданого теплоносителя в систему ЦО': 'to_system_co',
    #     'Объём обратного теплоносителя из системы ЦО': 'to_system_reverse_co',
    #     'Разница между подачей и обраткой(Подмес)': 'diff_between_feed_return_subset',
    #     'Разница между подачей и обраткой(Утечка)': 'diff_between_feed_return_leak',
    #     'Температура обратки': 'return_temperature',
    #     'Наработка часов счётчика': 'running_time_counter_clock',
    #     'Расход тепловой энергии ': 'thermal_energy_consumption',
    #     'Ошибки': 'errors', 'Марка счетчика': 'counter_mark'
    # }, inplace=True)
    # events_counter_all['error_description'] = events_counter_all['errors'].apply(lambda x: Utils.get_error_desc(x))
    # events_counter_all.fillna('Нет данных', inplace=True)

    outage = pd.read_excel(tables.get('6.xlsx'))
    outage.rename(columns={
        'Причина': 'reason', 'Источник': 'source',
        'Дата регистрации отключения': 'date_registration_shutdown',
        'Планируемая дата отключения': 'planned_shutdown_date',
        'Планируемая дата включения': 'planned_activation_date',
        'Фактическая дата отключения': 'fact_shutdown_date',
        'Фактическая дата включения': 'fact_activation_date',
        'Вид отключения': 'shutdown_type', 'УНОМ': 'unom', 'Адрес': 'address'}, inplace=True)

    energy_df = pd.read_excel(
        tables.get('12.xlsx'),
        usecols=["Департамент", "Класс энергоэффективности здания",
                 "Фактический износ здания, %", "Год ввода здания в эксплуатацию"])
    clear_shit = energy_df[~energy_df["Департамент"].astype(str).str.contains('^[А-Я]') == True]

    clear_shit["obj_consumer_address"] = clear_shit["Департамент"][2:].apply(lambda x: Utils.rename_address(x))
    clear_shit = clear_shit.drop(columns=["Департамент"])
    clear_shit.reset_index(drop=True, inplace=True)

    clear_shit.rename(columns={
        "Класс энергоэффективности здания": 'obj_consumer_energy_class',
        "Фактический износ здания, %": 'obj_consumer_building_wear_pct',
        "Год ввода здания в эксплуатацию": 'obj_consumer_build_date',
    }, inplace=True)

    res2 = res2.merge(clear_shit, how='left', on=["obj_consumer_address"])
    res2.fillna('Нет данных', inplace=True)

    counter_events = pd.read_excel(tables.get('11.xlsx'), sheet_name='Sheet 1')
    counter_events2 = pd.read_excel(tables.get('11.xlsx'), sheet_name='Sheet 2')
    errors_description = pd.read_excel(tables.get('11.xlsx'), sheet_name='Справочник Ошибки (W)')
    counter_events_all = pd.concat([counter_events, counter_events2])
    counter_events_all.rename(columns={
        'ID УУ': 'id_uu', 'ID ТУ': 'id_ty',
        'Округ': 'district', 'Район': 'area', 'Потребители': 'manager_company', 'Группа': 'group', 'UNOM': 'unom',
        'Адрес': 'address',
        'Центральное отопление(контур)': 'contour_co',
        'Марка счетчика ': 'counter_mark',
        'Марка счетчика': 'brand_counter',
        'Серия/Номер счетчика': 'number_counter',
        'Дата': 'date', 'Месяц/Год': 'month_year', 'Unit': 'unit',
        'Объём поданого теплоносителя в систему ЦО': 'obyom_podanogo_teplonositelya_v_sistemu_co',
        'Объём обратного теплоносителя из системы ЦО': 'obyom_obratnogo_teplonositelya_is_sistemu_co',
        'Разница между подачей и обраткой(Подмес)': 'podmes',
        'Разница между подачей и обраткой(Утечка)': 'ytechka',
        'Температура подачи': 'temp_podachi',
        'Температура обратки': 'temp_obratki',
        'Наработка часов счётчика': 'narabotka_chasov_schetchika',
        'Расход тепловой энергии ': 'rashod_teplovoy_energy',
        'Ошибки': 'errors'
    }, inplace=True)
    err_dict = errors_description.to_dict(orient='list')
    counter_events_all = AgrUnprocessed.get_err_counter_desc(counter_events_all, err_dict)
    counter_events_all.fillna(0, inplace=True)

    agr_tables['flat_table'] = res2
    agr_tables['events_all'] = events
    agr_tables['events_counter_all'] = counter_events_all
    agr_tables['outage'] = outage
    return agr_tables


class AgrView:
    @staticmethod
    def get_ranking(df: pd.DataFrame) -> pd.DataFrame:
        df['operation_mode_pr'] = df['operation_mode'].apply(lambda x: Utils.priority(x))
        df['sock_type_pr'] = df['sock_type'].apply(lambda x: Utils.priority(x))
        df['energy_class_pr'] = df['obj_consumer_energy_class'].apply(lambda x: Utils.priority(x))
        consumer_sources = df['obj_consumer_station_name'].unique().tolist()
        all_df = pd.DataFrame()
        for source in consumer_sources:
            new_df = df[df['obj_consumer_station_name'] == source]
            new_df['work_time_prior_rank'] = new_df[['operation_mode_pr']].apply(tuple, axis=1) \
                .rank(method='min', ascending=True).astype(int)
            new_df['build_type_prior_rank'] = new_df[['sock_type_pr']].apply(tuple, axis=1) \
                .rank(method='min', ascending=True).astype(int)
            new_df['energy_prior_rank'] = new_df[['energy_class_pr']].apply(tuple, axis=1) \
                .rank(method='min', ascending=True).astype(int)
            new_df['priority'] = new_df['work_time_prior_rank'] + new_df['build_type_prior_rank'] + new_df[
                'energy_prior_rank']
            new_df.sort_values(["priority", "obj_consumer_station_name"], inplace=True, ascending=True)
            all_df = pd.concat([all_df, new_df])
        all_df = all_df.drop(['work_time_prior_rank', 'build_type_prior_rank', 'energy_prior_rank',
                              'operation_mode_pr', 'sock_type_pr', 'energy_class_pr'], axis=1)
        return all_df

    @staticmethod
    def get_temp_conditions(df: pd.DataFrame) -> pd.DataFrame:
        df["temp_conditions"] = df["sock_type"].apply(lambda x: Utils.temp_conditions(x))
        return df

    @staticmethod
    def split_address(df: pd.DataFrame) -> pd.DataFrame:
        df['street'], df['house_number'], df['building'], df['section'] = \
            zip(*df['adres_potrebitelja'].map(Utils.parse_address))
        return df
        # df[df['street'].isnull()]

    @staticmethod
    def get_work_days(df: pd.DataFrame) -> pd.DataFrame:
        df['event_closed'] = df['event_closed'].astype('datetime64[ns]')
        df['event_created'] = df['event_created'].astype('datetime64[ns]')
        df['days_of_work'] = abs((df['event_closed'] - df['event_created']).dt.days.astype(float))
        return df

    @staticmethod
    def filter_events(df: pd.DataFrame, mask: pd.DataFrame) -> pd.DataFrame:
        masks = mask['event_name'].tolist()
        df = df[df['event_description'].isin(masks)]
        df['event_closed'].fillna(0, inplace=True)
        df['event_closed_ext'].fillna(0, inplace=True)
        df = df[(df['event_closed'] != 0) | (df['event_closed_ext'] != 0)]

        def event_closed_compare(x):
            if x['event_closed']:
                return x['event_closed']
            else:
                return x['event_closed_ext']

        df['event_closed'] = df.apply(lambda x: event_closed_compare(x), axis=1)
        df.drop(['event_closed_ext'], axis=1, inplace=True)
        return df

    @staticmethod
    def split_wall_materials(df: pd.DataFrame, df_wall_materials: pd.DataFrame) -> pd.DataFrame:
        df_wall_materials = df_wall_materials.rename(
            columns={"id": "material_sten", "name": "wall_material_description"})
        return df.merge(df_wall_materials, how='left', on='material_sten')

    @staticmethod
    def update_coordinates(df: pd.DataFrame) -> pd.DataFrame:
        df['obj_source_geodata_center'] = df['obj_source_geodata_center'].apply(
            lambda x: Utils.get_coord(x))
        df['obj_source_coordinates'] = df.apply(
            lambda x: Utils.compare_coord(x, 'obj_source_geodata_center', 'obj_source_geodata_center')
            , axis=1)
        df['obj_consumer_station_geodata_center'] = df['obj_consumer_station_geodata_center'].apply(
            lambda x: Utils.get_coord(x))
        df['obj_consumer_station_geodata'] = df['obj_consumer_station_geodata'].apply(
            lambda x: Utils.get_coord(x, darr=True))
        df['obj_consumer_geodata_center'] = df['obj_consumer_geodata_center'].apply(lambda x: Utils.get_coord(x))
        df['obj_consumer_geodata'] = df['obj_consumer_geodata'].apply(lambda x: Utils.get_coord(x, darr=True))
        df['obj_consumer_coordinates'] = df.apply(
            lambda x: Utils.compare_coord(x, 'obj_consumer_geodata_center', 'obj_consumer_geodata')
            , axis=1)
        df['obj_consumer_station_coordinates'] = df.apply(
            lambda x: Utils.compare_coord(x, 'obj_consumer_station_geodata_center', 'obj_consumer_station_geodata')
            , axis=1)
        df.drop(columns=[
            'obj_consumer_station_geodata_center', 'obj_consumer_station_geodata',
            'obj_consumer_geodata_center', 'obj_consumer_geodata',
        ], inplace=True)
        return df

    @staticmethod
    def clean_types(df: pd.DataFrame) -> pd.DataFrame:
        df['obj_consumer_is_dispatch'] = df['obj_consumer_is_dispatch'].apply(lambda x: True if x == 'да' else False)
        df['obj_consumer_build_floors'] = df['obj_consumer_build_floors'].apply(
            lambda x: int(x) if x != 'Нет данных' else 1)
        df['obj_consumer_total_area'] = df['obj_consumer_total_area'].apply(
            lambda x: float(x.replace(',', '.')) if x != "Нет данных" else 0.0)
        df['obj_consumer_station_ods_id_yy'] = df['obj_consumer_station_ods_id_yy'].apply(
            lambda x: int(float(x)) if x != 'Нет данных' else 0)
        df['obj_consumer_building_wear_pct'] = df['obj_consumer_building_wear_pct'].apply(
            lambda x: float(x) if x != "Нет данных" else 0.0)
        df['obj_consumer_build_date'] = df['obj_consumer_build_date'].apply(
            lambda x: int(float(x)) if x != "Нет данных" else 0)
        return df

    @staticmethod
    def get_operation_mode(df: pd.DataFrame) -> pd.DataFrame:
        df['operation_mode'] = df['obj_consumer_target'].apply(lambda x: Utils.get_work_time(x))
        return df

    @staticmethod
    def get_sock(df: pd.DataFrame) -> pd.DataFrame:
        df['sock_type'] = df['obj_consumer_target'].apply(lambda x: Utils.get_sock_type(x))
        return df


class AgrTrain:
    @staticmethod
    def agr_date(df: pd.DataFrame) -> pd.DataFrame:
        df['year'] = df['event_created'].dt.year
        df['month'] = df['event_created'].dt.month
        df['season'] = df['month'] % 12 // 3 + 1
        df['day'] = df['event_created'].dt.day
        # df['work_time'] = (df['event_closed'] - df['event_created']).dt.days
        df['day_of_week'] = df['event_created'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        return df

    @staticmethod
    def get_work_class(df: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
        events = events.set_index('event_name').T.to_dict('index').get('id')
        keys = list(events.keys())
        df["accident"] = df["event_description"].apply(lambda x: Utils.put_down_class(x, events, keys))
        return df

    @staticmethod
    def get_work_classes_all(df: pd.DataFrame) -> pd.DataFrame:
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
        df["accident"] = df["event_name"].apply(lambda x: Utils.check_in_type(x, alpabet))
        return df

    @staticmethod
    def clear_data(df: pd.DataFrame) -> pd.DataFrame:
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
    def get_predict_data(df: pd.DataFrame) -> pd.DataFrame:
        time_now = datetime.datetime.now()
        df_predict = df.groupby("consumer_id", as_index=False).last(True)  # 83125
        df_predict['last_event_id'] = df_predict['event_id']
        # # between block
        # df_predict['event_created'] = df_predict.apply(lambda x: Utils.collect_the_date(x), axis=1)
        # df_predict['between_created'] = df_predict['event_created'].apply(lambda x: (time_now - x).days)
        # # between block

        df_predict['event_created'] = time_now
        df_predict = AgrTrain.agr_date(df_predict)

        df_predict = df_predict.drop(columns='event_created')
        df_predict = df_predict[df.columns.tolist()]
        df_predict = df_predict.drop(columns='event_id')
        return df_predict

    @staticmethod
    def get_train_data(df: pd.DataFrame) -> pd.DataFrame:
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


class AgrUnprocessed:
    @staticmethod
    def get_err_counter_desc(counter_events: pd.DataFrame, err_dict: dict) -> pd.DataFrame:
        counter_events['error_desc'] = counter_events['errors'].apply(lambda x: Utils.add_desc(x, err_dict))
        return counter_events
    @staticmethod
    def agr_bti(bti_df: pd.DataFrame) -> pd.DataFrame:
        bti_df.columns = bti_df.iloc[0]
        bti_df = bti_df[1:]
        bti_df.dropna(subset=['Улица'], inplace=True)
        bti_df.fillna("Нет данных", inplace=True)
        bti_df.columns = ['id', 'Город', 'Административный округ',
                          'Муниципальный округ', 'Населенный пункт',
                          'Улица', 'Тип номера дом', 'Номер дома',
                          'Номер корпуса', 'Тип номера строения/сооружения',
                          'Номер строения', 'UNOM', 'UNAD',
                          'Материал', 'Назначение', 'Класс', 'Тип', 'Этажность', 'Признак', 'Общая площадь',
                          ]
        bti_df['Адрес строения'] = bti_df.apply(lambda x: Utils.compare_addr(x), axis=1)
        bti_df['Адрес ТП'] = bti_df['Адрес строения'].__deepcopy__()
        return bti_df

    @staticmethod
    def agr_ods(ods_df: pd.DataFrame) -> pd.DataFrame:
        ods_df.rename(columns={
            'ЦТП': 'obj_consumer_station_name',
            '№ ОДС': 'obj_consumer_station_ods_name',
            'ID УУ': 'obj_consumer_station_ods_id_yy',
            'Адрес ОДС': 'obj_consumer_station_ods_address',
            'Потребитель (или УК)': 'obj_consumer_station_ods_manager_company',
        }, inplace=True)
        ods_df.drop_duplicates(subset=['obj_consumer_station_name'], inplace=True)
        return ods_df


work_time = {'жилое': 'Круглосуточно', 'блокированный жилой дом': 'Круглосуточно',
             'многоквартирный дом': 'Круглосуточно', 'гараж и котельная': 'Круглосуточно',
             'спецназначение': 'Круглосуточно', 'типография': 'Круглосуточно', 'техкорпус': 'Круглосуточно',
             'ТП': 'Круглосуточно', 'служ.корпусслужебное': 'Круглосуточно', 'аварийная служба': 'Круглосуточно',
             'учреждение и производство': 'Круглосуточно', 'административно-производственное': 'Круглосуточно',
             'административный корпус и котельная': 'Круглосуточно', 'инженерный корпус': 'Круглосуточно',
             'бойлерная': 'Круглосуточно', 'насосная станция': 'Круглосуточно', 'гараж и проходная': 'Круглосуточно',
             'бытовое здание': 'Круглосуточно', 'мастерская и склад': 'Круглосуточно', 'лаборатория': 'Круглосуточно',
             'гараж и склад': 'Круглосуточно', 'АТС': 'Круглосуточно', 'пожарное депо': 'Круглосуточно',
             'пленкохранилище': 'Круглосуточно', 'насосная': 'Круглосуточно', 'телемеханический центр': 'Круглосуточно',
             'диспетчерская': 'Круглосуточно', 'модуль': 'Круглосуточно', 'тепловой пункт': 'Круглосуточно',
             'блок-станция': 'Круглосуточно', 'рентгеновский архив': 'Круглосуточно', 'ВОХР': 'Круглосуточно',
             'ЦТП': 'Круглосуточно', 'пункт охраны': 'Круглосуточно', 'ФОК': 'Круглосуточно',
             'учебно-производственный комбинат': 'Круглосуточно', 'хозяйственный корпус': 'Круглосуточно',
             'станция мед.газа': 'Круглосуточно', 'прочее с производством': 'Круглосуточно',
             'проходная': 'Круглосуточно', 'котельная': 'Круглосуточно', 'склад и учреждение': 'Круглосуточно',
             'механический цех': 'Круглосуточно', 'производственно-бытовой корпус': 'Круглосуточно',
             'опорно-усилительная станция': 'Круглосуточно', 'склад,учреждение': 'Круглосуточно',
             'комбинат бытового обслуживания': 'Круглосуточно', 'хозблок': 'Круглосуточно', 'склад': 'Круглосуточно',
             'производственное': 'Круглосуточно', 'подстанция': 'Круглосуточно', 'дворец спорта': '9:00 - 21:00',
             'санаторий': '9:00 - 21:00', 'учреждение,мастерскиеподсобное': '9:00 – 18:00',
             'консультативная поликлинника': '9:00 - 21:00', 'детский санаторий': '9:00 – 18:00',
             'торговое и учреждение': '9:00 – 18:00', 'медвытрезвитель': 'Круглосуточно',
             'спортивная школа': '9:00 - 21:00', 'торговое и бытовое обслуживание': '9:00 - 21:00',
             'техникум': '9:00 - 21:00', 'дворец пионеров': '9:00 – 18:00', 'кафе,магазин': '9:00 - 21:00',
             'неотложная медпомощь': 'Круглосуточно', 'склад и гараж': 'Круглосуточно',
             'гараж-стоянка': 'Круглосуточно', 'универмаг': '9:00 - 21:00', 'дом культуры': '9:00 - 21:00',
             'молочная кухня': '9:00 – 18:00', 'хранилище': '9:00 - 21:00', 'женская консультация': '9:00 - 21:00',
             'кухня клиническая': '9:00 - 21:00', 'академия': '9:00 - 21:00', 'плавательный бассейн': '9:00 - 21:00',
             'ресторан': '9:00 - 21:00', 'общественное питание': '9:00 - 21:00', 'клуб': '9:00 - 21:00',
             'кафе-столовая': '9:00 - 21:00', 'тех.школа': '9:00 – 18:00', 'общественный туалет': '9:00 - 21:00',
             'кинотеатр': '9:00 - 21:00', 'уборная': '9:00 - 21:00', 'здание общественных организаций': '9:00 - 21:00',
             'школа-сад': '9:00 – 18:00', 'архив': '9:00 - 21:00', 'административное здание': '9:00 – 18:00',
             'прочее': '9:00 - 21:00', 'почта': '9:00 - 21:00', 'блок-пристройка начальных классов': '9:00 – 18:00',
             'бытовое': '9:00 - 21:00', 'школа-интернат': '9:00 – 18:00', 'бытовое обслуживание': '9:00 - 21:00',
             'центр реабилитации': 'Круглосуточно', 'университет': '9:00 - 21:00', 'приходская школа': '9:00 – 18:00',
             'медучилище': '9:00 - 21:00', 'бытовой корпус': '9:00 - 21:00', 'бомбоубежище': 'Круглосуточно',
             'подстанция скорой помощи': 'Круглосуточно', 'терапевтический корпус': 'Круглосуточно',
             'хирургический корпус': 'Круглосуточно', 'спальный корпус': 'Круглосуточно',
             'школа искусств': '9:00 - 21:00', 'спортивный корпус': '9:00 - 21:00', 'аптека': '9:00 - 21:00',
             'нежилое,ГПТУ': '9:00 – 18:00', 'учебный корпус': '9:00 - 21:00',
             'административно-бытовой корпус': '9:00 – 18:00', 'столовая': '9:00 - 21:00',
             'наркологический диспансер': '9:00 – 18:00', 'ПТУ': '9:00 - 21:00', 'бассейн и спортзал': '9:00 - 21:00',
             'паталого-анатомический корпус': '9:00 - 21:00', 'лечебно-трудовые мастерские': '9:00 – 18:00',
             'интернат': '9:00 - 21:00', 'отдел милиции': 'Круглосуточно', 'пищеблок': '9:00 - 21:00',
             'зубной кабинет': '9:00 - 21:00', 'мойка автомашин': '9:00 - 21:00', 'ГАИ': 'Круглосуточно',
             'отделение милиции': 'Круглосуточно', 'химчистка': '9:00 - 21:00', 'спортивное': '9:00 - 21:00',
             'булочная-кондитерская': '9:00 - 21:00', 'гостиница': 'Круглосуточно', 'банк': '9:00 - 21:00',
             'дом ребенка': '9:00 - 21:00', 'детские ясли': '9:00 – 18:00', 'учебно-производственное': '9:00 - 21:00',
             'институт': '9:00 - 21:00', 'детсад-ясли': '9:00 – 18:00', 'административный корпус': '9:00 – 18:00',
             'военкомат': '9:00 – 18:00', 'лечебный корпус': '9:00 - 21:00', 'ясли-сад': '9:00 – 18:00',
             'родильный дом': 'Круглосуточно', 'научное': '9:00 - 21:00', 'универсам': '9:00 - 21:00',
             'станция скорой помощи': 'Круглосуточно', 'музей': '9:00 - 21:00', 'детская поликлиника': '9:00 - 21:00',
             'профтехучилище': '9:00 - 21:00', 'стоматологическая поликлиника': '9:00 - 21:00',
             'общежитие': 'Круглосуточно', 'спортзал': '9:00 - 21:00', 'кафе': '9:00 - 21:00',
             'музыкальная школа': '9:00 - 21:00', 'торговое и бытовое': '9:00 - 21:00', 'школьное': '9:00 – 18:00',
             'пекарня': '9:00 - 21:00', 'учебно-воспитательное': '9:00 - 21:00', 'учебное': '9:00 - 21:00',
             'училище': '9:00 - 21:00', 'оздоровительный комплекс': '9:00 - 21:00',
             'гражданская оборона': '9:00 - 21:00', 'торговый центр': '9:00 - 21:00',
             'центр обслуживания': '9:00 - 21:00', 'культурно-просветительное': '9:00 - 21:00',
             'дворец бракосочетания': '9:00 - 21:00', 'больница': 'Круглосуточно', 'морг': 'Круглосуточно',
             'парикмахерская': '9:00 - 21:00', 'колледж': '9:00 - 21:00',
             'учебно-воспитателный комбинат': '9:00 - 21:00', 'профилакторий': '9:00 - 21:00',
             'спортивный комплекс': '9:00 - 21:00', 'лечебное': '9:00 - 21:00', 'библиотека': '9:00 - 21:00',
             'поликлиника': '9:00 - 21:00', 'молочно-раздаточный пункт': '9:00 – 18:00',
             'отделение связи': '9:00 - 21:00', 'магазин': '9:00 - 21:00', 'торговое': '9:00 - 21:00',
             'административное': '9:00 – 18:00', 'гараж': 'Круглосуточно', 'учебно-научное': '9:00 - 21:00',
             'мастерская': '9:00 - 21:00', 'учреждение': '9:00 - 21:00', 'школа': '9:00 – 18:00',
             'физкультурно-оздоровительный комплекс': '9:00 - 21:00', 'ателье': '9:00 - 21:00',
             'детское дошкольное учреждение': '9:00 – 18:00', 'гимназия': '9:00 – 18:00', 'детский сад': '9:00 – 18:00',
             'церковь': '9:00 - 21:00', 'нежилое': 'Круглосуточно'}

material_dict = {
    'из железобетонных сегментов': 0.849775847370430,
    'панели керамзитобетонные': 0.94081687762476,
    'панельные': 0.84977584737043,
    'кирпичные': 0.97984936103377,
    'из унифицированных железобетонных элементов': 0.84977584737043,
    'из легкобетонных панелей': 0.89371490725226,
    'монолитные (ж-б)': 0.747126436781610,
    'железобетонные': 0.84977584737043,
    'крупнопанельные': 0.84977584737043,
    'металлические': 0.72984936103377,
    'смешанные': 0.88699221817663,
    'шлакобетонные': 0.89371490725226,
    'крупноблочные': 0.84977584737043,
    'из мелких бетонных блоков': 0.75265350209981,
    'легкобетонные блоки': 0.75265350209981,
    'деревянные': 0.75265350209981,
    'каркасно-панельные': 0.82345746442182,
    'бетонные': 0.89371490725226,
    'панельного типа несущие': 0.88699221817663,
    'Нет данных': 0.84977584737043,
    'каменные и бетонные': 0.93890859448325,
    'легкобетонные блоки с утеплением': 0.72984936103377,
    'из прочих материалов': 0.84977584737043,
    'монолитные (бетонные)': 1.0622198092134,
    'панели типа "Сэндвич"': 0.74712643678161,
    'кирпичные облегченные': 0.72984936103377,
    'каркасно-засыпные': 0.84977584737043,
    'железобетонный каркас': 0.84977584737043
}

errors = {
    'U': 'Отсутствие электропитания',
    'D': 'Разница температур в подающем и обратном трубопроводах меньше минимального',
    'g': 'Расход меньше минимального',
    'G': 'Расход больше максимального',
    'E': 'Функциональный отказ',
}

consumer_soc_type = {
    "Социальный": ['дворец спорта', 'санаторий', 'учреждение,мастерские' 'подсобное', 'консультативная поликлинника',
                   'детский санаторий', 'торговое и учреждение', 'медвытрезвитель', 'спортивная школа',
                   'торговое и бытовое обслуживание',
                   'техникум', 'дворец пионеров', 'кафе,магазин', 'неотложная медпомощь', 'склад и гараж',
                   'гараж-стоянка', 'универмаг', 'дом культуры', 'молочная кухня', 'хранилище', 'женская консультация',
                   'кухня клиническая', 'академия', 'плавательный бассейн', 'ресторан', 'общественное питание',
                   'клуб', 'кафе-столовая', 'тех.школа', 'общественный туалет', 'кинотеатр', 'уборная',
                   'здание общественных организаций',
                   'школа-сад', 'архив', 'административное здание', 'прочее', 'почта',
                   'блок-пристройка начальных классов', 'бытовое',
                   'школа-интернат', 'бытовое обслуживание', 'центр реабилитации', 'университет', 'приходская школа',
                   'медучилище', 'бытовой корпус', 'бомбоубежище', 'подстанция скорой помощи', 'терапевтический корпус',
                   'хирургический корпус', 'спальный корпус', 'школа искусств', 'спортивный корпус', 'аптека',
                   'нежилое,ГПТУ', 'учебный корпус', 'административно-бытовой корпус', 'столовая',
                   'наркологический диспансер',
                   'ПТУ', 'бассейн и спортзал', 'паталого-анатомический корпус', 'лечебно-трудовые мастерские',
                   'интернат',
                   'отдел милиции', 'пищеблок', 'зубной кабинет', 'мойка автомашин', 'ГАИ', 'отделение милиции',
                   'химчистка',
                   'спортивное', 'булочная-кондитерская', 'гостиница', 'банк', 'дом ребенка', 'детские ясли',
                   'учебно-производственное',
                   'институт', 'детсад-ясли', 'административный корпус', 'военкомат', 'лечебный корпус', 'ясли-сад',
                   'родильный дом', 'научное', 'универсам', 'станция скорой помощи', 'музей', 'детская поликлиника',
                   'профтехучилище', 'стоматологическая поликлиника', 'общежитие', 'спортзал', 'кафе',
                   'музыкальная школа',
                   'торговое и бытовое', 'школьное', 'пекарня', 'учебно-воспитательное', 'учебное', 'училище',
                   'оздоровительный комплекс', 'гражданская оборона', 'торговый центр', 'центр обслуживания',
                   'культурно-просветительное', 'дворец бракосочетания', 'больница', 'морг', 'парикмахерская',
                   'колледж', 'учебно-воспитателный комбинат', 'профилакторий', 'спортивный комплекс', 'лечебное',
                   'библиотека', 'поликлиника', 'молочно-раздаточный пункт', 'отделение связи', 'магазин',
                   'торговое', 'административное', 'гараж', 'учебно-научное', 'мастерская', 'учреждение',
                   'школа', 'физкультурно-оздоровительный комплекс', 'ателье', 'детское дошкольное учреждение',
                   'гимназия',
                   'детский сад', 'церковь', 'нежилое'],

    "Промышленный": ['гараж и котельная', 'спецназначение', 'типография', 'техкорпус', 'ТП', 'служ.корпус' 'служебное',
                     'аварийная служба', 'учреждение и производство', 'административно-производственное',
                     'административный корпус и котельная',
                     'инженерный корпус', 'бойлерная', 'насосная станция', 'гараж и проходная', 'бытовое здание',
                     'мастерская и склад', 'лаборатория', 'гараж и склад', 'АТС', 'пожарное депо', 'пленкохранилище',
                     'насосная', 'телемеханический центр', 'диспетчерская', 'модуль', 'тепловой пункт', 'блок-станция',
                     'рентгеновский архив', 'ВОХР', 'ЦТП', 'пункт охраны', 'ФОК', 'учебно-производственный комбинат',
                     'хозяйственный корпус', 'станция мед.газа', 'прочее с производством', 'проходная', 'котельная',
                     'склад и учреждение', 'механический цех', 'производственно-бытовой корпус',
                     'опорно-усилительная станция', 'склад,учреждение', 'комбинат бытового обслуживания', 'хозблок',
                     'склад', 'производственное', 'подстанция'],

    "МКД": ['жилое', 'блокированный жилой дом', 'многоквартирный дом']
}


class Utils:
    @staticmethod
    def add_desc(x, err_dict):
        res = []
        try:
            codes = x.split(',')
            for code in codes:
                try:
                    idx = err_dict.get('Код').index(code)
                    res.append(err_dict.get('Описание')[idx])
                except:
                    continue
            return ",".join(res)
        except:
            return "na"
    @staticmethod
    def get_sock_type(x):
        for k in consumer_soc_type:
            if x in consumer_soc_type[k]:
                return k
        return "Социальный"

    @staticmethod
    def get_work_time(x):
        return work_time.get(x)

    @staticmethod
    def compare_coord(x, center, polygon) -> dict:
        return {"center": x[center], 'polygon': x[polygon]}

    @staticmethod
    def priority(x):
        energy_classes = {
            'A': 0,
            'A+': 0,
            'A++': 0,
            'B': 1,
            'C': 2,
            'D': 2,
            'E': 2,
            'G': 2,
            'F': 2,
        }
        if energy_classes.get(x):
            return energy_classes.get(x)

        match x:
            case 'Круглосуточно':
                return 1
            case '9:00 - 21:00':
                return 2
            case '9:00 – 18:00':
                return 3
            case 'Социальный':
                return 1
            case 'Промышленный':
                return 2
            case 'МКД':
                return 3
            case _:
                return 3

    @staticmethod
    def temp_conditions(x):
        match x:
            case "Социальный":
                return dict(
                    summer_high=25.0,
                    summer_low=22.0,
                    winter_high=22.0,
                    winter_low=20.0,
                )
            case "МКД":
                return dict(
                    summer_high=22.0,
                    summer_low=20.0,
                    winter_high=20.0,
                    winter_low=18.0,
                )
            case "Промышленный":
                return dict(
                    summer_high=20.0,
                    summer_low=18.0,
                    winter_high=21.0,
                    winter_low=19.0,
                )
            case _:
                return dict(
                    summer_high=22.0,
                    summer_low=20.0,
                    winter_high=20.0,
                    winter_low=18.0,
                )

        # match x:
        #     case "Детский сад":
        #         return dict(summer=22.0, winter=20.0)
        #     case "Школа":
        #         return dict(summer=22.0, winter=20.0)
        #     case "Поликлиника":
        #         return dict(summer=22.0, winter=20.0)
        #     case "Теарт":
        #         return dict(summer=22.0, winter=20.0)
        #     case "Колледж":
        #         return dict(summer=22.0, winter=20.0)
        #     case _:
        #         return dict(summer=18.0, winter=18.0)

    @staticmethod
    def parse_address(x):
        new_xxx = [xx.strip() for xx in x.strip().split(",")]
        address = [new_xxx.pop(0), None, None, None]
        new_xxx = [xx.replace(" ", "") for xx in new_xxx]
        for new_x in new_xxx:
            if "д." in new_x or "вл." in new_x:
                address[1] = new_x.split('.')[-1]
            elif "к." in new_x or "корп." in new_x:
                address[2] = new_x.split('.')[-1]
            elif "с." in new_x or "стр." in new_x:
                address[3] = new_x.split('.')[-1]
        return address

        # return [street, house_number, building, section]

    @staticmethod
    def put_down_class(x: str, events: dict, keys: list) -> int:
        if x in keys:
            return events.get(x)
            # return 1
        return 0

    @staticmethod
    def collect_the_date(x):
        return datetime.datetime(int(x['year']), int(x['month']), int(x['day']))

    @staticmethod
    def compare_addr(x):
        addrs = []
        if x['Населенный пункт'] != 'Нет данных':
            addrs.append(x['Населенный пункт'].replace('посёлок', 'пос.'))
        if x['Улица'] != 'Нет данных':
            street = x['Улица']
            street = street.replace('улица', 'ул.')
            street = street.replace('проспект', 'просп.')
            street = street.replace('проезд', 'пр.')
            street = street.replace('набережная', 'наб.')
            street = street.replace('переулок', 'пер.')
            street = street.replace('площадь', 'пл.')
            street = street.replace('бульвар', 'бульв.')
            addrs.append(street)
        if x['Номер дома'] != 'Нет данных':
            d_type = x['Тип номера дом']
            d_type = re.sub('^дом$', 'д.', d_type)
            d_type = re.sub('^сооружение$', 'соор.', d_type)
            d_type = re.sub('^владение$', 'вл.', d_type)
            # домовладение
            addrs.append(f"{d_type}{x['Номер дома']}")
        if x['Номер корпуса'] != 'Нет данных':
            addrs.append(f"корп.{x['Номер корпуса']}")
        if x['Номер строения'] != 'Нет данных':
            str_type = x['Тип номера строения/сооружения']
            str_type = str_type.replace('строение', 'стр.')
            str_type = str_type.replace('сооружение', 'соор.')
            addrs.append(f"{str_type}{x['Номер строения']}")

        return ', '.join(addrs)

    @staticmethod
    def get_coord(x, darr=False):
        res = []
        if isinstance(x, str):
            numbers = re.findall(r'[\d\.\-]+', x)
            try:
                if darr:
                    tmp = []
                    for i in numbers:
                        tmp.append(float(i))
                        if len(tmp) == 2:
                            # tmp.reverse()
                            res.append(tmp)
                            tmp = []
                else:
                    res = [float(num) for num in numbers]
                    # res.reverse()
            except ValueError:
                return x
            else:
                return res
        else:
            return x

    @staticmethod
    def set_obj_source_station_coord(x):
        coord = []
        match x:
            case 'ТЭЦ №23':
                coord = ["Монтажная ул., 1/4с1", 37.764117, 55.821649]
            case 'ТЭЦ №22':
                coord = ["ул. Энергетиков, 5, Дзержинский", 37.816665, 55.630469]
            case 'РТС Перово':
                coord = ["Кетчерская ул., 11А", 37.837246, 55.747464]
            case 'ТЭЦ №11':
                coord = ["шоссе Энтузиастов, 32с1", 37.730223, 55.752803]
            case 'КТС-42':
                coord = ["Гражданская 4-я ул., д. 41", 37.719944, 55.807567]
            case 'КТС-28':
                coord = ["Бойцовая ул., д. 24", 37.727607, 55.814801]
            case 'КТС Акулово':
                coord = ["пос. Акулово, д.30А", 37.794460, 56.006502]
        return coord

    @staticmethod
    def get_addr(x):
        adr = x.pop(0)
        return adr

    @staticmethod
    def get_source_data(source: str) -> tuple[int, int, int, int]:
        # (Электрическая мощность, Тепловая мощность, Котлы, Турбогенераторы)
        return {
            'ТЭЦ №23': (1420, 3709, 23, 8),
            'РТС Перово': (0, 391, 4, 0),
            'ТЭЦ №22': (1070, 3402, 22, 11),
            'ТЭЦ №11': (330, 868, 7, 3),
            'КТС-42': (0, 25, 4, 0),
            'КТС Акулово': (0, 8, 4, 0),
            'КТС-28': (0, 28, 4, 0),
        }.get(source, (0, 0, 0, 0))

    @staticmethod
    def check_heat_resist(material: str) -> float:
        if material in material_dict:
            return material_dict[material]
        else:
            return 0.82345746442182

    @staticmethod
    def get_error_desc(x):
        errs = []
        try:
            for err in x.split(','):
                errs.append(errors.get(err, 'Нет данных'))
        finally:
            if errs:
                return ','.join(errs)
            else:
                return 'Нет данных'

    @staticmethod
    def rename_address(address: str) -> str:
        """Indian Magic! Don't touch!!!!"""
        if isinstance(address, str):
            split_address = address.split(' ')
            try:
                type_a = split_address[0]
                if type_a == 'пр-кт':
                    type_a = 'просп.'
                elif type_a == 'ш.':
                    type_a = 'шоссе'
                elif type_a == 'б-р':
                    type_a = 'бульвар'
                elif type_a == 'пл.':
                    type_a = 'площадь'
                elif type_a == 'наб.':
                    type_a = 'набережная'
                elif type_a == 'проезд':
                    type_a = 'пр.'
                else:
                    type_a = split_address[0]

                house_type = 'д.'
                if split_address[1][0].isupper() and split_address[2][0].isupper() and split_address[2] not in ["Б.",
                                                                                                                "М."]:
                    if split_address[3][0].isdigit():
                        name_a = split_address[3] + ' ' + split_address[1] + ' ' + split_address[2]
                        if split_address[4] not in ["Б.", "М."]:
                            house_number = split_address[5]
                            try:
                                if split_address[6] == "стр.":
                                    str_num = split_address[7]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', стр.' + str_num
                                elif split_address[6] == "корп.":
                                    corp_num = split_address[7]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', корп.' + corp_num
                            except:
                                pass
                        else:
                            house_number = split_address[6]
                            try:
                                if split_address[7] == "стр.":
                                    str_num = split_address[8]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', стр.' + str_num
                                elif split_address[7] == "корп.":
                                    corp_num = split_address[8]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', корп.' + corp_num
                            except:
                                pass
                    else:
                        name_a = split_address[1] + ' ' + split_address[2]
                        if split_address[3] not in ["Б.", "М."]:
                            house_number = split_address[4]
                            try:
                                if split_address[5] == "стр.":
                                    str_num = split_address[6]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', стр.' + str_num
                                elif split_address[5] == "корп.":
                                    corp_num = split_address[6]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', корп.' + corp_num
                            except:
                                pass
                        else:
                            house_number = split_address[5]
                            try:
                                if split_address[6] == "стр.":
                                    str_num = split_address[7]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', стр.' + str_num
                                elif split_address[6] == "корп.":
                                    corp_num = split_address[7]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', корп.' + corp_num
                            except:
                                pass
                else:
                    if split_address[2][0].isdigit():
                        name_a = split_address[2] + ' ' + split_address[1]
                        if split_address[3] not in ["Б.", "М."]:
                            house_number = split_address[4]
                        else:
                            house_type = split_address[4]
                            house_number = split_address[5]
                        try:
                            if split_address[6] == "стр.":
                                str_num = split_address[7]
                                return name_a + ' ' + type_a + ', ' + house_type + house_number + ', стр.' + str_num
                            elif split_address[6] == "корп.":
                                corp_num = split_address[7]
                                return name_a + ' ' + type_a + ', ' + house_type + house_number + ', корп.' + corp_num
                        except:
                            pass
                    else:
                        name_a = split_address[1]
                        if split_address[2] not in ["Б.", "М."]:
                            house_number = split_address[3]
                            try:
                                if split_address[4] == "стр.":
                                    str_num = split_address[5]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', стр.' + str_num
                                elif split_address[4] == "корп.":
                                    corp_num = split_address[5]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', корп.' + corp_num
                            except:
                                pass
                        else:
                            house_number = split_address[4]
                            try:
                                if split_address[5] == "стр.":
                                    str_num = split_address[6]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', стр.' + str_num
                                elif split_address[5] == "корп.":
                                    corp_num = split_address[6]
                                    return name_a + ' ' + type_a + ', ' + house_type + house_number + ', корп.' + corp_num
                            except:
                                pass
                return name_a + ' ' + type_a + ', ' + house_type + house_number
            except:
                return address
    # @staticmethod
    # def put_down_class(x: str, events: list) -> int:
    #     if x in events:
    #         return 1
    #     return 0
    #
    # @staticmethod
    # def check_in_type(x: str, alpabet: dict) -> int:
    #     alpabet.keys()
    #     scores = {}
    #     for k, v in alpabet.items():
    #         for tp in v:
    #             if not isinstance(x, str) or x == '':
    #                 scores['Другое'] = scores['Другое'] + 1 if scores.get('Другое') else 1
    #                 continue
    #             if tp in x:
    #                 if scores.get(k):
    #                     scores[k] += 1
    #                 else:
    #                     scores[k] = 1
    #     # print('Очки', scores)
    #     if scores:
    #         # return max(scores, key=scores.get)
    #         res = max(scores, key=scores.get)
    #         if res == 'Другое':
    #             return 30
    #         return list(alpabet.keys()).index(res)
    #     else:
    #         return -1


def upload(file, name):
    job = get_current_job()
    df = pd.ExcelFile(file, )
    job.meta[name] = df
    job.save_meta()
