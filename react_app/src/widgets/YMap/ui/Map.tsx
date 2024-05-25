import {useMemo, useState} from "react";

import cls from './map.module.scss'

import {classNames} from "@src/shared/lib/classNames";
import {ErrorWrapper} from "@src/entities/errorWrapper";

import {YMapLocationRequest} from "@yandex/ymaps3-types";

import {MapMenu} from './mapMenu/MapMenu';
import {MapContext} from '../model/context'
import {coordinates} from "../const/coordinates";

import {
    YMap,
    YMapDefaultSchemeLayer,
    YMapDefaultFeaturesLayer,
    YMapControls,
    YMapScaleControl
} from '../const/mapInit'
import {useGetAreasQuery} from "../api/getAreas";

export const Map = () => {
    const [location, setLocation] = useState<YMapLocationRequest>({center: coordinates.moscow, zoom: 11})

    const {data, isFetching, error} = useGetAreasQuery()

    const contextVal = useMemo(() => {
        return {
            setLocation,
            location
        }
    }, [setLocation, location])

    return (
        <MapContext.Provider value={contextVal}>
            <div className={classNames(cls.map_wrapper)}>
                <ErrorWrapper
                    snackBarErrors={{
                        errors: [{error: true, message: 'Не удалось загрузить данные'}]
                    }}
                >
                    <MapMenu/>
                </ErrorWrapper>
                <div className={classNames(cls.map)}>
                    <YMap
                        location={location}
                        mode="vector"
                        zoomRounding="smooth"
                    >
                        <YMapDefaultSchemeLayer/>
                        <YMapDefaultFeaturesLayer/>
                        <YMapControls position='top right'>
                            <YMapScaleControl/>
                        </YMapControls>
                    </YMap>
                </div>
            </div>
        </MapContext.Provider>
    )
}