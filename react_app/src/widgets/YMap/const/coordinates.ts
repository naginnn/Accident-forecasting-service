import {LngLat} from "ymaps3";

export type CountyCoordinates = {
    name: string
    value: LngLat
}

type Coordinates = {
    moscow: LngLat
    districts: Record<string, LngLat>
    countyCoordinates: CountyCoordinates[]

}
export const coordinates: Coordinates = {
    moscow: [37.617617, 55.755811],
    districts: {
        'VAO': [37.775631, 55.787715]
    },
    countyCoordinates: [
        {
            name: 'Восточный административный округ',
            value: [37.775631, 55.787715]
        },
        {
            name: 'Северо-Восточный административный округ',
            value: [37.632565, 55.854875]
        },
    ]
}