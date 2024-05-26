import {FC} from "react";

import {Divider, Typography} from "@mui/material";

import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {SourceStations, Weather} from "../types/consumerCorrelationsInfo";
import {conditionRuVal, windDirRuVal} from "../const/weatherRuVal";
import {CollapsedBlock} from "@src/entities/collapsedBlock";

interface CommonInfoBlockProps {
    weather: Weather | null
    areaName: string | undefined
    srcStations: SourceStations[] | null
    consumerStationName: string | undefined
    consumerStationAddr: string | undefined
}

export const CommonInfoBlock: FC<CommonInfoBlockProps> = (
    {
        weather,
        areaName,
        srcStations,
        consumerStationName,
        consumerStationAddr
    }) => {
    return (
        <PaperWrapper>
            <Typography variant='h5' gutterBottom>
                Общая информация
            </Typography>
            <Divider/>
            {
                areaName &&
                <Typography sx={{mt: '8px'}} gutterBottom component='div'>
                    <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                        Местоположение:&nbsp;
                    </Typography>
                    {areaName}
                </Typography>
            }
            {
                (consumerStationName || consumerStationAddr) &&
                <Typography sx={{mt: '8px'}} gutterBottom component='div'>
                    <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                        ЦТП:&nbsp;
                    </Typography>
                    {consumerStationName},&nbsp;
                    {consumerStationAddr}
                </Typography>
            }
            {
                srcStations?.length &&
                <SrcStations data={srcStations}/>
            }
            {
                weather &&
                <WeatherInfo weather={weather}/>
            }
        </PaperWrapper>
    );
};

const SrcStations: FC<{ data: SourceStations[] }> = ({data}) => {
    return (
        <CollapsedBlock topicName='Источники тепла' textPlacement='right'>
            {
                data.map(srcStation => {
                    return <React.Fragment key={srcStation.id}>
                        <Typography sx={{mt: '8px'}} gutterBottom>
                            {srcStation.name}, &nbsp;
                            {srcStation.address}
                        </Typography>
                        <Divider/>
                    </React.Fragment>
                })
            }
        </CollapsedBlock>
    )
}

const WeatherInfo: FC<{ weather: Weather }> = ({weather}) => {
    return <>
        <Typography gutterBottom sx={{fontWeight: 500}} variant='h6'>
            Погода
        </Typography>
        <Typography gutterBottom component='div'>
            <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                Температура:&nbsp;
            </Typography>
            {weather.temp} &deg;C, {conditionRuVal[weather.condition]}
        </Typography>
        <Typography gutterBottom component='div'>
            <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                Cкорость ветра:&nbsp;
            </Typography>
            {weather.wind_speed} км/ч
        </Typography>
        {
            weather.wind_dir in windDirRuVal &&
            <Typography gutterBottom component='div'>
                <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                    Направление ветра:&nbsp;
                </Typography>
                {windDirRuVal[weather.wind_dir]}
            </Typography>
        }
    </>
}
