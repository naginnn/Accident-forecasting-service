import pandas as pd
import re

from apps.train_api.src._test_utils import log
from apps.train_api.service.aggregate.config import (
    MATERIALS, COUNTER_EVENTS_COLUMNS_MAP, OUTAGE_COLUMNS_MAP, EVENTS_COLUMNS_MAP,
    FLAT_TABLE_COLUMNS_MAP, FLAT_TABLE_COLUMNS, BTI_COLUMNS, TP_COLUMNS,
    OBJ_SOURCE_COLUMNS, ODS_COLUMNS, ODS_COLUMNS_MAP, BTI_COLUMNS_FOR_AGR,
    SOURCE_STATION_INFO
)
from apps.train_api.service.aggregate.utils import Utils

pd.options.mode.chained_assignment = None  # default='warn'


class AgrUnprocessed:
    """ Класс для подготовки данных """
    @staticmethod
    @log
    def execute(tables) -> dict[str, pd.DataFrame]:
        """ Основной метод для получения агрегированных таблиц """

        # Создание плоской таблицы
        flat_table = AgrUnprocessed._get_flat_table(
            main=tables.get('7.xlsx'),     # Схема подключений МОЭК
            bti=tables.get('9.xlsx'),      # Выгрузка БТИ
            coords=tables.get("13.xlsx"),  # Адресный реестр объектов недвижимости города Москвы
            ods=tables.get('8.xlsx'),      # Данные АСУПР с диспетчерскими ОДС
            energy=tables.get('12.xlsx'),  # Класс энергоэффективности соцобъектов
        )

        # Перечень событий за период (ЦУ КГХ)
        events_all = AgrUnprocessed._get_events(
            events=(tables.get('5.xlsx'), tables.get('5.1.xlsx'))
        )

        # Выгрузка ОДПУ отопления
        events_counter_all = AgrUnprocessed._get_counter_events(
            counter_events=(tables.get('11.xlsx_1'), tables.get('11.xlsx_2')),
            errors_description=tables.get('11.xlsx_W')
        )

        # Плановые-Внеплановые отключения 01.10.2023-30.04.2023
        outage = AgrUnprocessed._get_outage(
            outage=tables.get('6.xlsx')
        )

        agr_tables = {
            'flat_table': flat_table,
            'events_all': events_all,
            'events_counter_all': events_counter_all,
            'outage': outage,
        }

        # test case
        # удалить после тестирования
        AgrUnprocessed._test_execute(agr_tables)

        return agr_tables

    @staticmethod
    def _test_execute(agr_tables: dict[str, pd.DataFrame]):
        """ Проверка результирующих таблиц """
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

    @staticmethod
    def _get_flat_table(
            main: pd.DataFrame, bti: pd.DataFrame, coords: pd.DataFrame,
            ods: pd.DataFrame, energy: pd.DataFrame) -> pd.DataFrame:
        """ Создание плоской таблицы """

        main_df = main

        # Выгрузка БТИ
        bti_df = AgrUnprocessed._agr_bti(bti)
        big_df = main_df.merge(bti_df[[*BTI_COLUMNS]], how="inner", on='Адрес строения')

        # Формируем таблицу для ТП
        tp_df = bti_df.__deepcopy__()
        tp_df.columns = TP_COLUMNS
        with_tp_df = big_df.merge(
            tp_df[['UNOM_ТП', 'Адрес ТП']], how="inner", on='Адрес ТП')

        # Адресный реестр объектов недвижимости города Москвы
        df_coord = coords
        df_coord = df_coord[1:]
        df_coord['UNOM'] = df_coord['UNOM'].astype(float)
        big_tp_coord = with_tp_df.merge(
            df_coord[['geoData', 'geodata_center', 'UNOM']], how="inner", on='UNOM')
        df_coord = df_coord.rename(
            columns={'UNOM': 'UNOM_ТП', 'geoData': 'geoData_ТП',
                     'geodata_center': 'geodata_center_ТП'}
        ).__deepcopy__()

        flat_table = big_tp_coord.merge(
            df_coord[['geoData_ТП', 'geodata_center_ТП', 'UNOM_ТП']],
            how="inner", on='UNOM_ТП')

        flat_table['geodata_center'] = flat_table['geodata_center'].apply(
            lambda x: Utils.get_coord(x))
        flat_table['geoData'] = flat_table['geoData'].apply(
            lambda x: Utils.get_coord(x, darr=True))
        flat_table['geodata_center_ТП'] = flat_table['geodata_center_ТП'].apply(
            lambda x: Utils.get_coord(x))
        flat_table['geoData_ТП'] = flat_table['geoData_ТП'].apply(
            lambda x: Utils.get_coord(x, darr=True))
        flat_table['Источник теплоснабжения'].unique().tolist()
        flat_table['geoData_ТЭЦ'] = flat_table['Источник теплоснабжения'].apply(
            lambda x: AgrUnprocessed._set_obj_source_station_coord(x))
        flat_table["Адрес ТЭЦ"] = flat_table['geoData_ТЭЦ'].apply(
            lambda x: AgrUnprocessed._get_addr(x))
        flat_table.rename(columns=FLAT_TABLE_COLUMNS_MAP, inplace=True)
        flat_table[[*OBJ_SOURCE_COLUMNS]] = flat_table['obj_source_name'].apply(
            lambda x: pd.Series(AgrUnprocessed._get_source_data(x)))
        flat_table = flat_table[[*FLAT_TABLE_COLUMNS]]

        # Данные АСУПР с диспетчерскими ОДС
        ods_df = AgrUnprocessed._agr_ods(ods)
        flat_table = flat_table.merge(
            ods_df[[*ODS_COLUMNS]], how='left', on='obj_consumer_station_name')
        flat_table.fillna("Нет данных", inplace=True)
        flat_table['wall_material_k'] = flat_table['wall_material'].apply(
            lambda x: AgrUnprocessed._check_heat_resist(x))

        # Класс энергоэффективности соцобъектов
        energy_df = energy

        clear_shit = energy_df[
            ~energy_df["Департамент"].astype(str).str.contains('^[А-Я]') == True]
        clear_shit["obj_consumer_address"] = clear_shit["Департамент"][2:].apply(
            lambda x: AgrUnprocessed._rename_address(x))
        clear_shit = clear_shit.drop(columns=["Департамент"])
        clear_shit.reset_index(drop=True, inplace=True)

        clear_shit.rename(columns={
            "Класс энергоэффективности здания": 'obj_consumer_energy_class',
            "Фактический износ здания, %": 'obj_consumer_building_wear_pct',
            "Год ввода здания в эксплуатацию": 'obj_consumer_build_date',
        }, inplace=True)

        flat_table = flat_table.merge(clear_shit, how='left', on=["obj_consumer_address"])
        flat_table.fillna('Нет данных', inplace=True)

        return flat_table

    @staticmethod
    def _get_events(events: tuple[pd.DataFrame, pd.DataFrame]) -> pd.DataFrame:
        """ Перечень событий (ЦУ КГХ)"""
        events[1].rename(columns={
            'Дата и время завершения события': 'Дата и время завершения события во внешней системе'},
            inplace=True)
        events_all = pd.concat([*events])
        events_all.rename(columns=EVENTS_COLUMNS_MAP, inplace=True)

        return events_all

    @staticmethod
    def _get_counter_events(counter_events: tuple, errors_description) -> pd.DataFrame:
        """Выгрузка ОДПУ отопления"""
        counter_events_all = pd.concat([*counter_events])
        counter_events_all.rename(columns=COUNTER_EVENTS_COLUMNS_MAP, inplace=True)
        err_dict = errors_description.to_dict(orient='list')
        counter_events_all = AgrUnprocessed._get_err_counter_desc(
            counter_events_all, err_dict)
        counter_events_all.fillna(0, inplace=True)

        return counter_events_all

    @staticmethod
    def _get_outage(outage: pd.DataFrame) -> pd.DataFrame:
        """Плановые-Внеплановые отключения"""
        outage.rename(columns=OUTAGE_COLUMNS_MAP, inplace=True)

        return outage

    @staticmethod
    @log
    def _get_err_counter_desc(counter_events: pd.DataFrame, err_dict: dict) -> pd.DataFrame:
        """ Обогощает таблицу описанием ошибки """
        counter_events['error_desc'] = counter_events['errors'].apply(lambda x: AgrUnprocessed._add_desc(x, err_dict))
        return counter_events

    @staticmethod
    def _add_desc(x, err_dict):
        """ Возвращает описание ошибки """
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
    @log
    def _agr_bti(bti_df: pd.DataFrame) -> pd.DataFrame:
        """ Подготовка таблицы БТИ """
        bti_df.columns = bti_df.iloc[0]
        bti_df = bti_df[1:]
        bti_df.dropna(subset=['Улица'], inplace=True)
        bti_df.fillna("Нет данных", inplace=True)
        bti_df.columns = BTI_COLUMNS_FOR_AGR
        bti_df['Адрес строения'] = bti_df.apply(lambda x: AgrUnprocessed._compare_addr(x), axis=1)
        bti_df['Адрес ТП'] = bti_df['Адрес строения'].__deepcopy__()
        return bti_df

    @staticmethod
    def _compare_addr(x):
        """ Возвращает преобразованный адрес: улица - ул., дом -> д. ..."""
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
            # домовладение не обрабатываем
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
    @log
    def _agr_ods(ods_df: pd.DataFrame) -> pd.DataFrame:
        """ Подготовка таблицы ODS """
        ods_df.rename(columns=ODS_COLUMNS_MAP, inplace=True)
        ods_df.drop_duplicates(subset=['obj_consumer_station_name'], inplace=True)
        return ods_df

    # UTILS
    @staticmethod
    def _set_obj_source_station_coord(source_name):
        """ Возвращает адрес и координаты станции """
        coords, _ = SOURCE_STATION_INFO.get(source_name, [])
        return coords[:]  # возвращаем копию [адрес, координаты]

    @staticmethod
    def _get_addr(x):
        return x.pop(0)

    @staticmethod
    def _get_source_data(source_name: str) -> tuple[int, int, int, int]:
        # (Электрическая мощность, Тепловая мощность, Котлы, Турбогенераторы)
        default = (0, 0, 0, 0)
        _, source_info = SOURCE_STATION_INFO.get(source_name, default)
        return source_info

    @staticmethod
    def _check_heat_resist(material: str) -> float:
        """ Возвращает коэф. теплопотерь """
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
