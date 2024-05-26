type Area = {
    id: number
    location_district_id: number
    name: string
    coordinates: string
    weather: null
    consumers: null
    source_stations: null
}

type ConsumerStations = {
    id: number
    location_district_id: number
    location_area_id: number
    name: string
    address: string
    coordinates: string
    source_stations: null
    consumers: null
    accidents: null
}

export type SourceStations = {
    id: number
    location_district_id: number
    location_area_id: number
    name: string
    address: string
    coordinates: string
    consumer_stations: null
}

type EventConsumer = {
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
}

export type Consumer = {
    id: number
    obj_consumer_station_id: number
    location_district_id: number
    location_area_id: number
    name: string
    address: string
    coordinates: string
    total_area: number
    living_area: number
    not_living_area: number
    type: string
    energy_class: string
    operating_mode: string
    priority: number
    temp_conditions: {
    summer_high: number
        summer_low: number
        winter_high: number
        winter_low: number
}
    accidents: null
    weather_fall: []
    events: EventConsumer[]
    wall_material: []
    roof_material: null
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