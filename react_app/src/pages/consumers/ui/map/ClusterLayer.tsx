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

import {PopupMarker} from "./PopupMarker";
import {CriticalStatusName, TransformConsumers} from "../../api/getConsumers";

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
                .filter(el => (el.critical_status !== CriticalStatusName.IS_NO_ACCENDENT))
                .map((el, i) => {
                    return {
                        id: `${i}`,
                        properties: {
                            info: el,
                        },
                        type: 'Feature',
                        geometry: {type: "Point", coordinates: el.consumer_geo_data}
                    } as Feature
                })
        }
    }, [data])

    const marker = useCallback(
        (feature: Feature) => {
            return (
                <PopupMarker
                    key={`${feature.id}`}
                    coordinates={feature.geometry.coordinates}
                    info={feature.properties?.info as TransformConsumers}
                />
            )
        },
        []
    );

    const cluster = useCallback((coordinates: LngLat, features: Feature[]) => {
        const warnTotal = features.reduce((total, curr) => {
            //@ts-ignore
            if (curr?.properties?.info?.critical_status === CriticalStatusName.IS_WARNING)
                return total + 1
            return total
        }, 0)

        const approvedTotal = features.reduce((total, curr) => {
            //@ts-ignore
            if (curr?.properties?.info?.critical_status === CriticalStatusName.IS_APPROVED)
                return total + 1
            return total
        }, 0)

        return (
            <YMapMarker
                key={`${features[0].id}-${features.length}`}
                coordinates={coordinates}
                source="clusterer-source"
                zIndex={1800}
            >
                <>
                    <Paper
                        onClick={() => {
                            setLocation({
                                center: features[0].geometry.coordinates,
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
                                    {warnTotal}
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
                                    {approvedTotal}
                                </Typography>
                            </Box>
                        }
                    </Paper>
                </>
            </YMapMarker>
        )
    }, []);

    if (!points)
        return null

    return (
        <>
            <YMapFeatureDataSource id="clusterer-popup-source"/>
            <YMapLayer source="clusterer-popup-source" type="markers" zIndex={1900}/>
            <YMapFeatureDataSource id="clusterer-source"/>
            <YMapLayer source="clusterer-source" type="markers" zIndex={1800}/>
            <YMapClusterer
                maxZoom={17}
                marker={marker}
                cluster={cluster}
                method={gridSizedMethod}
                features={points}
            />
        </>
    );
};
