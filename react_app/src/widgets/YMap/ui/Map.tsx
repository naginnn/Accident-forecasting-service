import {FC, useCallback, useEffect, useMemo, useState} from "react";

import cls from './map.module.scss'

import {classNames} from "@src/shared/lib/classNames";

import {YMapLocationRequest} from "@yandex/ymaps3-types";

import {MapContext} from '../model/context'

import {
    YMap,
    YMapDefaultSchemeLayer,
    YMapDefaultFeaturesLayer,
    YMapControls,
    YMapScaleControl,
    YMapZoomControl,
    YMapControlButton,
    YMapListener
} from '../const/mapInit'
import {useGetAreasQuery} from "../api/getAreas";

window.map = null;

interface IMapProps {
    location: YMapLocationRequest
    setLocation: React.Dispatch<React.SetStateAction<YMapLocationRequest>>
    children?: any
}

export const Map: FC<IMapProps> = ({location, setLocation, children}) => {
    const [isFullscreen, setIsFullscreen] = useState(false);

    useEffect(() => {
        const onFullscreenChange = () => {
            setIsFullscreen(Boolean(document.fullscreenElement));
        };
        document.addEventListener('fullscreenchange', onFullscreenChange);

        return () => document.removeEventListener('fullscreenchange', onFullscreenChange);
    }, []);

    const onUpdate = useCallback(({location}: {location: YMapLocationRequest}) => setLocation(location), []);

    const onClickHandler = useCallback(() => {
        if (isFullscreen) {
            document.exitFullscreen();
        } else if (window.map) {
            debugger
            window.map.container.requestFullscreen();
        }
    }, [isFullscreen]);

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
                {/*<ErrorWrapper*/}
                {/*    snackBarErrors={{*/}
                {/*        errors: [{error: true, message: 'Не удалось загрузить данные'}]*/}
                {/*    }}*/}
                {/*>*/}
                {/*    <MapMenu/>*/}
                {/*</ErrorWrapper>*/}
                <div className={classNames(cls.map, {[cls.map_fullscreen]: isFullscreen})}>
                    <YMap
                        location={location}
                        mode="vector"
                        zoomRounding="smooth"
                        ref={(x) => (window.map = x)}
                    >
                        <YMapListener onUpdate={onUpdate}/>
                        <YMapDefaultSchemeLayer/>
                        <YMapDefaultFeaturesLayer/>
                        <YMapControls position="right">
                            <YMapZoomControl/>
                        </YMapControls>
                        <YMapControls position='top left'>
                            <YMapScaleControl/>
                        </YMapControls>
                        <YMapControls position="top right">
                            <YMapControlButton onClick={onClickHandler}>
                                <div className={
                                    classNames(cls.fullscreen, {[cls.exitFullscreen]: isFullscreen})
                                }/>
                            </YMapControlButton>
                        </YMapControls>
                        {children}
                    </YMap>
                </div>
            </div>
        </MapContext.Provider>
    )
}