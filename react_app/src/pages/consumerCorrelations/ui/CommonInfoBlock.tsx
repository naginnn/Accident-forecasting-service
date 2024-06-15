import {FC} from "react";

import HolidayVillageIcon from '@mui/icons-material/HolidayVillage';

import {Box, Divider, Typography} from "@mui/material";

import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {Weather} from "../types/consumerCorrelationsInfo";
import {conditionRuVal, windDirRuVal} from "../const/weatherRuVal";
import {weatherConditionIcons, windDirIcons} from "../const/weatherIcons";
import FactoryIcon from "@mui/icons-material/Factory";

interface CommonInfoBlockProps {
    weather: Weather | null
    areaName: string | undefined
    consumerStationName: string | undefined
    consumerStationAddr: string | undefined
}

export const CommonInfoBlock: FC<CommonInfoBlockProps> = (
    {
        weather,
        areaName,
        consumerStationName,
        consumerStationAddr
    }) => {
    return (
        <PaperWrapper sx={{mt: 0}}>
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
                <Box sx={{mt: '5.6px', display: 'flex', alignItems: 'center', gap: '8px'}}>
                    <HolidayVillageIcon sx={{color: '#039be5'}}/>
                    <Typography sx={{mt: '8px'}} gutterBottom component='div'>
                    <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                        ЦТП:&nbsp;
                    </Typography>
                        {consumerStationName},&nbsp;
                        {consumerStationAddr}
                </Typography>
                </Box>

            }
            {
                weather &&
                <WeatherInfo weather={weather}/>
            }
        </PaperWrapper>
    );
};

const WeatherInfo: FC<{ weather: Weather }> = ({weather}) => {
    return <>
        <Typography gutterBottom sx={{fontWeight: 500}} variant='h6'>
            Погода
        </Typography>
        <Box sx={{display: 'flex', alignItems: 'center', gap: '4px', mb: '5.6px'}}>
            <Typography component='div'>
                <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                    Температура:&nbsp;
                </Typography>
                {weather.temp} &deg;C, {conditionRuVal[weather.condition as unknown as keyof typeof conditionRuVal]}
            </Typography>
            {weatherConditionIcons[weather.condition as unknown as keyof typeof conditionRuVal]}
        </Box>
        <Typography gutterBottom component='div'>
            <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                Cкорость ветра:&nbsp;
            </Typography>
            {weather.wind_speed} км/ч
        </Typography>
        {
            weather.wind_dir in windDirRuVal &&
            <Box sx={{display: 'flex', alignItems: 'center', gap: '4px'}}>
                <Typography component='div'>
                    <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                        Направление ветра:&nbsp;
                    </Typography>
                    {windDirRuVal[weather.wind_dir as unknown as keyof typeof windDirRuVal]}
                </Typography>
                {windDirIcons[weather.wind_dir as unknown as keyof typeof windDirRuVal]}
            </Box>
        }
    </>
}
