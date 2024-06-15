import {FC, useState} from "react";
import {YMapLocationRequest} from "ymaps3";

import {Box, Button, Paper} from "@mui/material";

import {coordinates} from "@src/widgets/YMap/const/coordinates";
import {YMap, YMapControl, YMapControls} from "@src/widgets/YMap";

import {ConsumerStationPopup} from "./ConsumerStationPopup";
import {SourceStationPopup} from "./SourceStationPopup";
import {ConsumersPopupPolygon} from "./ConsumersPopupPolygon";
import {FormattedConsumer} from "../../types/formattedConsumer";
import {FormattedConsumerCorrelationsInfo} from "../../api/getConsumerCorrelations";

interface ConsumersMapProps {
    info: FormattedConsumerCorrelationsInfo
    setActiveConsumer: React.Dispatch<React.SetStateAction<FormattedConsumer | undefined>>
}

export const ConsumersMap: FC<ConsumersMapProps> = ({info, setActiveConsumer}) => {
    const [showAllConsumers, setShowAllConsumers] = useState<boolean>(true)
    const [location, setLocation] = useState<YMapLocationRequest>(() => {
        let center = coordinates.districts.VAO

        if (info.consumer_stations?.geo_data.center) {
            center = info.consumer_stations.geo_data.center
        } else if (info.consumers_dep?.length) {
            center = info.consumers_dep[0].geo_data.center
        }

        return {center, zoom: 15}
    })

    const getConsumersPolygon = () => {
        if (info.consumers_dep?.length) {
            if (showAllConsumers) {
                return info.consumers_dep.map(el => {
                    return <ConsumersPopupPolygon key={el.id} info={el} setActiveConsumer={setActiveConsumer}/>
                })
            }
        }
    }

    return (
        <Box sx={{height: '600px', width: '100%', position: 'relative', mt: '16px'}}>
            <YMap
                location={location}
                setLocation={setLocation}
            >
                <YMapControls position="top">
                    <YMapControl>
                        <Paper>
                            <Button
                                variant='main-outlined'
                                sx={{border: 'none'}}
                                onClick={() => setShowAllConsumers(prev => !prev)}
                            >
                                {
                                    showAllConsumers
                                        ? 'Скрыть всех потребителей'
                                        : 'Показать всех потребителей'
                                }
                            </Button>
                        </Paper>
                    </YMapControl>
                </YMapControls>
                {
                    info.consumer_stations &&
                    <ConsumerStationPopup
                        info={info.consumer_stations}
                    />
                }
                {
                    info.source_stations?.length &&
                    info.source_stations.map(el => {
                        return <SourceStationPopup
                            key={el.id}
                            info={el}
                        />
                    })
                }
                {
                    getConsumersPolygon()
                }
            </YMap>
        </Box>
    );
};
