import cls from './clusterLayer.module.css'

import {FC, useCallback, useMemo} from "react";
import {LngLat, YMapLocationRequest} from "ymaps3";
import type {Feature} from '@yandex/ymaps3-clusterer';
import {red, orange} from "@mui/material/colors";

import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";

import {Box, Paper, Typography} from "@mui/material";

import {
    clusterByGrid,
    YMapClusterer,
    YMapLayer,
    YMapMarker,
    YMapFeatureDataSource, pointInBound,
} from "@src/widgets/YMap";
import {classNames} from "@src/shared/lib/classNames";

import {PolygonPopupMarker} from "./PolygonPopupMarker";
import {TransformConsumers} from "../../api/getConsumers";

interface ClusterLayerProps {
    setLocation: React.Dispatch<React.SetStateAction<YMapLocationRequest>>
    location: YMapLocationRequest
    data: TransformConsumers[]
}

export const ClusterLayer: FC<ClusterLayerProps> = ({setLocation, data, location}) => {
    const gridSizedMethod: any = useMemo(() => {
        //@ts-ignore
        return clusterByGrid({gridSize: 128})
    }, []);

    const points: Feature[] | undefined = useMemo(() => {
        if (data?.length) {
            return data
                .filter(el => (el.is_warning || el.is_approved || el.is_approved))
                .map((el) => {
                return {
                    id: `${el.consumer_station_id}`,
                    properties: {
                        critical_status: el.critical_status,
                        polygon: el.consumer_geo_data.polygon
                    },
                    type: 'Feature',
                    geometry: {type: "Point", coordinates: el.consumer_geo_data.center}
                } as Feature
            })
        }
    }, [data])

    const cluster = useCallback((coordinates: LngLat, features: Feature[]) => {
        const warnTotal = features.reduce((total, curr) => {
            //@ts-ignore
            if (curr?.properties?.is_warning)
                return total + 1
            return total
        }, 0)

        const approvedTotal = features.reduce((total, curr) => {
            //@ts-ignore
            if (curr?.properties?.is_approved)
                return total + 1
            return total
        }, 0)

        return (
            <YMapMarker
                key={`${features[0].id}-${features.length}`}
                coordinates={coordinates}
                source="clusterer-source"
            >
                <>
                    {
                        approvedTotal || warnTotal
                            ? <Paper
                                onClick={() => {
                                    setLocation({
                                        center: coordinates,
                                        zoom: 17
                                    })
                                }}
                                sx={{p: '4px'}}
                            >
                                {
                                    !!warnTotal &&
                                    <Box sx={{
                                        p: '4px',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '4px',
                                        cursor: 'pointer'
                                    }}>
                                        <WarningAmberIcon sx={{color: orange[600]}}/>
                                        <Typography sx={{display: 'block', width: 'max-content'}}>
                                            {warnTotal} / {features.length}
                                        </Typography>
                                    </Box>
                                }
                                {
                                    !!approvedTotal &&
                                    <Box sx={{
                                        p: '4px',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '4px',
                                        cursor: 'pointer'
                                    }}>
                                        <ErrorOutlineIcon sx={{color: red[600]}}/>
                                        <Typography sx={{display: 'block', width: 'max-content'}}>
                                            {approvedTotal} / {features.length}
                                        </Typography>
                                    </Box>
                                }
                            </Paper>
                            : <div
                                className={classNames(cls.circle)}
                                onClick={() => {
                                    setLocation({
                                        center: features[0]?.geometry?.coordinates || coordinates,
                                        zoom: 17
                                    })
                                }}
                            >
                                <div className={classNames(cls['circle-content'])}>
                                    <span className={classNames(cls['circle-text'])}>{features.length}</span>
                                </div>
                            </div>
                    }
                </>
            </YMapMarker>
        )
    }, []);

    const getPolygonMarkers = () => {
        if (points?.length && 'zoom' in location && 'bounds' in location && location.zoom >= 15) {
            return points.filter(el => {
                //@ts-ignore
                return pointInBound(el.geometry.coordinates, location.bounds)
            }).map((el, i) => {
                return (
                    <PolygonPopupMarker
                        key={`${i}`}
                        id={`${i}`}
                        isApproved={false}
                        isWarning={false}
                        center={el.geometry.coordinates}
                        polygon={el.properties?.polygon as unknown as LngLat[]}
                    />
                )
            })
        }

        return null
    }

    if (!points)
        return null

    return (
        <>
            <YMapFeatureDataSource id="clusterer-source"/>
            <YMapLayer source="clusterer-source" type="markers" zIndex={1800}/>
            <YMapClusterer
                maxZoom={15}
                marker={() => <></>}
                cluster={cluster}
                method={gridSizedMethod}
                features={points}
            />
            {getPolygonMarkers()}
        </>
    );
};
