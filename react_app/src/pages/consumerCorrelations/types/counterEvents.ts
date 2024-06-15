export type CounterEvent = {
    id: number
    obj_consumer_id: number
    event_consumer_id: number
    contour: string
    counter_mark: string
    counter_number: number
    created: string
    gcal_in_system: number
    gcal_out_system: number
    subset: number
    leak: number
    supply_temp: number
    return_temp: number
    work_hours_counter: number
    heat_thermal_energy: number
    errors: string
    errors_desc: string
}