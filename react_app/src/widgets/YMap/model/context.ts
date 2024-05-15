import {createContext} from "react";

import {YMapLocationRequest} from "ymaps3";

import {coordinates} from '../const/coordinates'

interface IMapContext {
    location: YMapLocationRequest
    setLocation: (location: YMapLocationRequest) => void
}

const defaultContext: IMapContext = {
    location: {
        center: coordinates.moscow,
        zoom: 11
    },
    setLocation: (location) => null
}

export const MapContext = createContext<IMapContext>(defaultContext);