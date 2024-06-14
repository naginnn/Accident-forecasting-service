import {LngLat} from "ymaps3";

type Area = {
    id: number
    location_district_id: number
    name: string
    coordinates: string
    weather: null
    consumers: null
    source_stations: null
}

export type ConsumerStations = {
    id: number
    location_district_id: number
    location_area_id: number
    name: string
    address: string
    coordinates: string
    source_stations: null
    consumers: null
    accidents: null
    ods_address: string
    ods_manager_company: string
    ods_name: string
    place_type: string
    type: string
    geo_data: {
        center: LngLat
        polygon: LngLat[]
    }
}

export type SourceStations = {
    id: number
    address: string
    boiler_count: number
    e_power: number
    launched_date: string
    location_area_id: number
    location_district_id: number
    name: string
    t_power: number
    turbine_count: number
    geo_data: {
        center: LngLat
        polygon: LngLat[]
    }
}

export type EventConsumer = {
    id: number
    obj_consumer_id: number
    source: string
    description: string
    is_approved: boolean
    is_closed: boolean
    probability: number
    days_of_work: number
    created: string
    closed: string
    events_counter: number | null
}

type WallMaterial = {
    id: number
    consumers: null
    k: number
    name: string
}

export type TempDropping = {
    date_ts: number
    temp: number
}

type WeatherFall = {
    created: string
    id: number
    obj_consumer_id: number
    temp_dropping: {
        temp_data: TempDropping[]
    }
}

export type Consumer = {
    address: string
    b_class: string
    balance_holder: string
    build_year: number
    corpus_number: string
    energy_class: string
    events: EventConsumer[] | null
    events_counter: number | null
    floors: number
    geo_data: {
        center: LngLat
        polygon: LngLat[]
    }
    heat_load: string
    house_number: string
    house_type: string
    id: number
    is_dispatch: boolean
    load_fact: string
    load_gvs: string
    location_area_id: number
    location_district_id: number
    number: string
    obj_consumer_station_id: number
    operating_mode: string
    priority: number
    sock_type: string
    soor_number: string
    soor_type: string
    street: string
    target: string
    temp_conditions: {
        summer_high: number
        summer_low: number
        winter_high: number
        winter_low: number
    }
    total_area: number
    type: string
    vent_load: string
    wall_material: WallMaterial[]
    wear_pct: string
    weather_fall: WeatherFall[]
}

export type Weather = {
    temp: number
    wind_speed: number
    wind_dir: string
    humidity: number
    condition: string
}

export type ConsumerCorrelationsInfo = {
    area: Area | null
    consumer_stations: ConsumerStations | null
    consumer_warn: Consumer[] | null
    consumers_dep: Consumer[] | null
    source_stations: SourceStations[] | null
    weather: Weather | null
}