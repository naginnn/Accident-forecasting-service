import pandas as pd
from apps.train_api.src._test_utils import log
from apps.train_api.service.aggregate.config import CONSUMER_SOC_TYPE, WORK_TIME, DISTRICT_LOCATION
from apps.train_api.service.aggregate.utils import Utils

pd.options.mode.chained_assignment = None  # default='warn'


class AgrView:
    @staticmethod
    @log
    def execute(tables: dict) -> dict:
        """Агрегация данных"""
        agr_tables = {}
        flat_table = tables.get('flat_table')
        events_all = tables.get('events_all')
        event_types = tables.get('event_types')
        events_counter_all = tables.get('events_counter_all')
        outage = tables.get('outage')
        flat_table = AgrView._update_coordinates(flat_table)
        flat_table = AgrView._clean_types(flat_table)
        flat_table = AgrView._get_operation_mode(flat_table)
        flat_table = AgrView._get_sock(flat_table)
        flat_table = AgrView._get_ranking(flat_table)
        flat_table = AgrView._get_temp_conditions(flat_table)
        flat_table = AgrView._get_area_coord(flat_table)
        # flat_table = AgrView.get_temp_conditions(flat_table)
        # flat_table = AgrView.split_address(flat_table)
        # flat_table = AgrView.split_wall_materials(flat_table, df_wall_materials)
        # df_events = tables.get('test_events_all')
        # df_events = AgrView.get_work_days(df_events)
        events_all = AgrView._filter_events(events_all, event_types)
        events_all = AgrView._get_work_days(events_all)

        events_counter_all['month_year'] = events_counter_all[
            'month_year'].astype('datetime64[ns]')
        agr_tables["flat_table"] = flat_table
        agr_tables["events_all"] = events_all
        agr_tables["events_counter_all"] = events_counter_all
        agr_tables["outage"] = outage
        return agr_tables

    @staticmethod
    @log
    def _get_area_coord(df: pd.DataFrame) -> pd.DataFrame:
        df['location_area_coord'] = df['obj_consumer_station_location_area'].apply(lambda x: AgrView._get_coord_by_area(x))
        return df
    @staticmethod
    @log
    def _get_coord_by_area(x):
        return DISTRICT_LOCATION.get(x, "55.753544 37.621202")
    @staticmethod
    @log
    def _get_ranking(df: pd.DataFrame) -> pd.DataFrame:
        df['operation_mode_pr'] = df['operation_mode'].apply(lambda x: AgrView._priority(x))
        df['sock_type_pr'] = df['sock_type'].apply(lambda x: AgrView._priority(x))
        df['energy_class_pr'] = df['obj_consumer_energy_class'].apply(lambda x: AgrView._priority(x))
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
    @log
    def _get_temp_conditions(df: pd.DataFrame) -> pd.DataFrame:
        df["temp_conditions"] = df["sock_type"].apply(lambda x: AgrView._temp_conditions(x))
        return df

    @staticmethod
    @log
    def _split_address(df: pd.DataFrame) -> pd.DataFrame:
        df['street'], df['house_number'], df['building'], df['section'] = \
            zip(*df['adres_potrebitelja'].map(AgrView._parse_address))
        return df
        # df[df['street'].isnull()]

    @staticmethod
    @log
    def _get_work_days(df: pd.DataFrame) -> pd.DataFrame:
        df['event_closed'] = df['event_closed'].astype('datetime64[ns]')
        df['event_created'] = df['event_created'].astype('datetime64[ns]')
        df['days_of_work'] = abs((df['event_closed'] - df['event_created']).dt.days.astype(float))
        return df

    @staticmethod
    @log
    def _filter_events(df: pd.DataFrame, mask: pd.DataFrame) -> pd.DataFrame:
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
    @log
    def _split_wall_materials(df: pd.DataFrame, df_wall_materials: pd.DataFrame) -> pd.DataFrame:
        df_wall_materials = df_wall_materials.rename(
            columns={"id": "material_sten", "name": "wall_material_description"})
        return df.merge(df_wall_materials, how='left', on='material_sten')

    @staticmethod
    @log
    def _update_coordinates(df: pd.DataFrame) -> pd.DataFrame:
        df['obj_source_geodata_center'] = df['obj_source_geodata_center'].apply(
            lambda x: Utils.get_coord(x))
        df['obj_source_coordinates'] = df.apply(
            lambda x: AgrView._compare_coord(x, 'obj_source_geodata_center', 'obj_source_geodata_center')
            , axis=1)
        df['obj_consumer_station_geodata_center'] = df['obj_consumer_station_geodata_center'].apply(
            lambda x: Utils.get_coord(x))
        df['obj_consumer_station_geodata'] = df['obj_consumer_station_geodata'].apply(
            lambda x: Utils.get_coord(x, darr=True))
        df['obj_consumer_geodata_center'] = df['obj_consumer_geodata_center'].apply(lambda x: Utils.get_coord(x))
        df['obj_consumer_geodata'] = df['obj_consumer_geodata'].apply(lambda x: Utils.get_coord(x, darr=True))
        df['obj_consumer_coordinates'] = df.apply(
            lambda x: AgrView._compare_coord(x, 'obj_consumer_geodata_center', 'obj_consumer_geodata')
            , axis=1)
        df['obj_consumer_station_coordinates'] = df.apply(
            lambda x: AgrView._compare_coord(x, 'obj_consumer_station_geodata_center', 'obj_consumer_station_geodata')
            , axis=1)
        df.drop(columns=[
            'obj_consumer_station_geodata_center', 'obj_consumer_station_geodata',
            'obj_consumer_geodata_center', 'obj_consumer_geodata',
        ], inplace=True)
        return df

    @staticmethod
    @log
    def _clean_types(df: pd.DataFrame) -> pd.DataFrame:
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
    @log
    def _get_operation_mode(df: pd.DataFrame) -> pd.DataFrame:
        df['operation_mode'] = df['obj_consumer_target'].apply(lambda x: AgrView._get_work_time(x))
        return df

    @staticmethod
    @log
    def _get_sock(df: pd.DataFrame) -> pd.DataFrame:
        df['sock_type'] = df['obj_consumer_target'].apply(lambda x: AgrView._get_sock_type(x))
        return df

    # Utils
    @staticmethod
    def _get_sock_type(x):
        for k in CONSUMER_SOC_TYPE:
            if x in CONSUMER_SOC_TYPE[k]:
                return k
        return "Социальный"

    @staticmethod
    def _get_work_time(x):
        return WORK_TIME.get(x)

    @staticmethod
    def _compare_coord(x, center, polygon) -> dict:
        return {"center": x[center], 'polygon': x[polygon]}

    @staticmethod
    def _priority(x):
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
    def _temp_conditions(x):
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

    @staticmethod
    def _parse_address(x):
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
