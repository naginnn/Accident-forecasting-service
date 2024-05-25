export interface Consumers {
    SourceStationId: number
    source_station_name: string
    source_station_address: string
    source_station_coordinates: string
    consumer_station_id: number
    consumer_station_name: string
    consumer_station_address: string
    consumer_station_coordinates: string
    location_district_consumer_id: number
    location_district_consumer_name: string
    location_area_consumer_id: number
    location_area_consumer_name: string
    location_area_consumer_coordinates: string
    consumer_id: number
    consumer_name: string
    consumer_address: string
    consumer_coordinates: string
    source: string
    description: string
    probability: number
    is_approved: boolean
    is_closed: boolean
    is_warning: boolean
}
