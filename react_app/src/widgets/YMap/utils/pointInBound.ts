import {LngLat, LngLatBounds} from "ymaps3";

export const pointInBound = (point: LngLat, bound: LngLatBounds): boolean => {
    if (point[0] >= bound[0][0] && point[0] <= bound[1][0] &&
        point[1] <= bound[0][1] && point[1] >= bound[1][1]
    ) {
        return true
    }

    return true
}