import pandas as pd
import re

from apps.train_api.src._test_utils import log
from apps.train_api.service.aggregate.config import MATERIALS
from apps.train_api.service.aggregate.utils import Utils

pd.options.mode.chained_assignment = None  # default='warn'


class AgrUnprocessed:
    @staticmethod
    @log
    def execute(tables: dict[str, pd.ExcelFile]) -> dict[str, pd.DataFrame]:
        agr_tables = {}

        # Схема подключений МОЭК
        main_df = tables.get('7.xlsx')

        # Выгрузка БТИ
        bti_df = AgrUnprocessed._agr_bti(tables.get('9.xlsx'))
        big_df = main_df.merge(bti_df[[
            'UNOM', 'Адрес строения',
            'Административный округ', 'Муниципальный округ',
            'Улица', 'Тип номера дом', 'Номер дома',
            'Номер корпуса', 'Тип номера строения/сооружения',
            'Номер строения',
            'Материал', 'Назначение', 'Класс', 'Тип', 'Этажность',
            'Общая площадь',
            # ]], how="left", on='Адрес строения')
        ]], how="inner", on='Адрес строения')
        tp_df = bti_df.__deepcopy__()
        tp_df.columns = ['id_ТП', 'Город_ТП', 'Административный округ_ТП',
                         'Муниципальный округ_ТП', 'Населенный пункт_ТП',
                         'Улица_ТП', 'Тип номера дом_ТП', 'Номер дома_ТП',
                         'Номер корпуса_ТП',
                         'Тип номера строения/сооружения_ТП',
                         'Номер строения_ТП', 'UNOM_ТП', 'UNAD_ТП',
                         'Материал_ТП', 'Назначение_ТП', 'Класс_ТП', 'Тип_ТП',
                         'Этажность_ТП', 'Признак_ТП',
                         'Общая площадь_ТП', 'Адрес строения ТП', 'Адрес ТП'
                         ]
        with_tp_df = big_df.merge(tp_df[['UNOM_ТП', 'Адрес ТП']], how="inner",
                                  on='Адрес ТП')

        # Адресный реестр объектов недвижимости города Москвы
        df_coord = tables.get("13.xlsx")
        df_coord = df_coord[1:]
        df_coord['UNOM'] = df_coord['UNOM'].astype(float)
        res = with_tp_df.merge(df_coord[['geoData', 'geodata_center', 'UNOM']],
                               how="inner", on='UNOM')
        df_coord = df_coord.rename(
            columns={'UNOM': 'UNOM_ТП', 'geoData': 'geoData_ТП',
                     'geodata_center': 'geodata_center_ТП'}).__deepcopy__()
        res2 = res.merge(
            df_coord[['geoData_ТП', 'geodata_center_ТП', 'UNOM_ТП']],
            how="inner", on='UNOM_ТП')
        res2['geodata_center'] = res2['geodata_center'].apply(
            lambda x: Utils.get_coord(x))
        res2['geoData'] = res2['geoData'].apply(
            lambda x: Utils.get_coord(x, darr=True))
        res2['geodata_center_ТП'] = res2['geodata_center_ТП'].apply(
            lambda x: Utils.get_coord(x))
        res2['geoData_ТП'] = res2['geoData_ТП'].apply(
            lambda x: Utils.get_coord(x, darr=True))
        res2['Источник теплоснабжения'].unique().tolist()
        res2['geoData_ТЭЦ'] = res2['Источник теплоснабжения'].apply(
            lambda x: AgrUnprocessed._set_obj_source_station_coord(x))
        res2["Адрес ТЭЦ"] = res2['geoData_ТЭЦ'].apply(
            lambda x: AgrUnprocessed._get_addr(x))
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
        res2[[*obj_source_columns]] = res2['obj_source_name'].apply(
            lambda x: pd.Series(AgrUnprocessed._get_source_data(x)))

        res2 = res2[[
            # source station
            'obj_source_name', 'obj_source_launched', 'obj_source_address',
            'obj_source_e_power',
            'obj_source_t_power',
            'obj_source_boiler_count',
            'obj_source_turbine_count',
            'obj_source_geodata_center',
            # consumer_station
            'obj_consumer_station_location_district',
            'obj_consumer_station_location_area', 'obj_consumer_station_name',
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

        # Данные АСУПР с диспетчерскими ОДС
        ods_df = AgrUnprocessed._agr_ods(tables.get('8.xlsx'))
        res2 = res2.merge(ods_df[['obj_consumer_station_name',
                                  'obj_consumer_station_ods_name',
                                  'obj_consumer_station_ods_address',
                                  'obj_consumer_station_ods_id_yy',
                                  'obj_consumer_station_ods_manager_company',
                                  ]], how='left',
                          on='obj_consumer_station_name')
        res2.fillna("Нет данных", inplace=True)
        res2['wall_material_k'] = res2['wall_material'].apply(
            lambda x: AgrUnprocessed._check_heat_resist(x))

        # Перечень событий за период  (ЦУ КГХ)
        events = tables.get('5.xlsx')
        # Перечень событий за период  (ЦУ КГХ)
        events2 = tables.get('5.1.xlsx')
        events2.rename(columns={
            'Дата и время завершения события': 'Дата и время завершения события во внешней системе'},
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

        # Плановые-Внеплановые отключения 01.10.2023-30.04.2023
        outage = tables.get('6.xlsx')
        outage.rename(columns={
            'Причина': 'reason', 'Источник': 'source',
            'Дата регистрации отключения': 'date_registration_shutdown',
            'Планируемая дата отключения': 'planned_shutdown_date',
            'Планируемая дата включения': 'planned_activation_date',
            'Фактическая дата отключения': 'fact_shutdown_date',
            'Фактическая дата включения': 'fact_activation_date',
            'Вид отключения': 'shutdown_type', 'УНОМ': 'unom',
            'Адрес': 'address'}, inplace=True)

        # Класс энергоэффективности соцобъектов
        energy_df = tables.get('12.xlsx')

        clear_shit = energy_df[
            ~energy_df["Департамент"].astype(str).str.contains(
                '^[А-Я]') == True]

        clear_shit["obj_consumer_address"] = clear_shit["Департамент"][
                                             2:].apply(
            lambda x: AgrUnprocessed._rename_address(x))
        clear_shit = clear_shit.drop(columns=["Департамент"])
        clear_shit.reset_index(drop=True, inplace=True)

        clear_shit.rename(columns={
            "Класс энергоэффективности здания": 'obj_consumer_energy_class',
            "Фактический износ здания, %": 'obj_consumer_building_wear_pct',
            "Год ввода здания в эксплуатацию": 'obj_consumer_build_date',
        }, inplace=True)

        res2 = res2.merge(clear_shit, how='left', on=["obj_consumer_address"])
        res2.fillna('Нет данных', inplace=True)

        # Выгрузка ОДПУ отопления
        counter_events = tables.get('11.xlsx_1')
        counter_events2 = tables.get('11.xlsx_2')
        errors_description = tables.get('11.xlsx_W')
        counter_events_all = pd.concat([counter_events, counter_events2])
        counter_events_all.rename(columns={
            'ID УУ': 'id_uu', 'ID ТУ': 'id_ty',
            'Округ': 'district', 'Район': 'area',
            'Потребители': 'manager_company', 'Группа': 'group',
            'UNOM': 'unom',
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
        counter_events_all = AgrUnprocessed._get_err_counter_desc(
            counter_events_all, err_dict)
        counter_events_all.fillna(0, inplace=True)

        agr_tables['flat_table'] = res2
        agr_tables['events_all'] = events
        agr_tables['events_counter_all'] = counter_events_all
        agr_tables['outage'] = outage
        print('agr_tables', agr_tables)
        print(type(outage))

        # start test case
        tests = {
            'flat_table': (5575, 49),   # rows, cols
            'events_all': (916483, 8),
            'events_counter_all': (1004375, 25),
            'outage': (115, 10),
        }

        err = False
        for tbl, df in agr_tables.items():
            rows = len(df.index)
            cols = len(df.columns)
            if tests.get(tbl) != (rows, cols):
                err = True
                print('NO GOOD', (rows, cols), 'must be = ', (tests.get(tbl)))

        if not err:
            print('Test Agregate.execute: PASS')
        else:
            print('Test Agregate.execute: NO PASS')
        # end test case

        return agr_tables

    @staticmethod
    @log
    def _get_err_counter_desc(counter_events: pd.DataFrame, err_dict: dict) -> pd.DataFrame:
        counter_events['error_desc'] = counter_events['errors'].apply(lambda x: AgrUnprocessed._add_desc(x, err_dict))
        return counter_events

    @staticmethod
    @log
    def _agr_bti(bti_df: pd.DataFrame) -> pd.DataFrame:
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
        bti_df['Адрес строения'] = bti_df.apply(lambda x: AgrUnprocessed._compare_addr(x), axis=1)
        bti_df['Адрес ТП'] = bti_df['Адрес строения'].__deepcopy__()
        return bti_df

    @staticmethod
    @log
    def _agr_ods(ods_df: pd.DataFrame) -> pd.DataFrame:
        ods_df.rename(columns={
            'ЦТП': 'obj_consumer_station_name',
            '№ ОДС': 'obj_consumer_station_ods_name',
            'ID УУ': 'obj_consumer_station_ods_id_yy',
            'Адрес ОДС': 'obj_consumer_station_ods_address',
            'Потребитель (или УК)': 'obj_consumer_station_ods_manager_company',
        }, inplace=True)
        ods_df.drop_duplicates(subset=['obj_consumer_station_name'], inplace=True)
        return ods_df

    # UTILS
    @staticmethod
    def _add_desc(x, err_dict):
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
    def _compare_addr(x):
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
    def _set_obj_source_station_coord(x):
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
    def _get_addr(x):
        adr = x.pop(0)
        return adr

    @staticmethod
    def _get_source_data(source: str) -> tuple[int, int, int, int]:
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
    def _check_heat_resist(material: str) -> float:
        if material in MATERIALS:
            return MATERIALS[material]
        else:
            return 0.82345746442182

    @staticmethod
    def _rename_address(address: str) -> str:
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
