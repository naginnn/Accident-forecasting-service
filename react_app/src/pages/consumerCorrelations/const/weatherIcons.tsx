import {ReactElement} from "react";

import SouthIcon from '@mui/icons-material/South';
import SouthEastIcon from '@mui/icons-material/SouthEast';
import SouthWestIcon from '@mui/icons-material/SouthWest';
import NorthIcon from '@mui/icons-material/North';
import NorthWestIcon from '@mui/icons-material/NorthWest';
import NorthEastIcon from '@mui/icons-material/NorthEast';
import EastIcon from '@mui/icons-material/East';
import WestIcon from '@mui/icons-material/West';

import WbCloudyIcon from '@mui/icons-material/WbCloudy';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import FilterDramaIcon from '@mui/icons-material/FilterDrama';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import AcUnitIcon from '@mui/icons-material/AcUnit';
import AirIcon from '@mui/icons-material/Air';
import ThunderstormIcon from '@mui/icons-material/Thunderstorm';

import {conditionRuVal, windDirRuVal} from "./weatherRuVal";

export const windDirIcons: Record<keyof typeof windDirRuVal, ReactElement> = {
    's': <SouthIcon fontSize='small'/>,
    'n': <NorthIcon fontSize='small'/>,
    'w': <WestIcon fontSize='small'/>,
    'e': <EastIcon fontSize='small'/>,
    'nw': <NorthWestIcon fontSize='small'/>,
    'ne': <NorthEastIcon fontSize='small'/>,
    'se': <SouthEastIcon fontSize='small'/>,
    'sw': <SouthWestIcon fontSize='small'/>,
}

export const weatherConditionIcons: Record<keyof typeof conditionRuVal, ReactElement> = {
    'clear': <WbSunnyIcon fontSize='small'/>,
    'partly-cloudy': <WbCloudyIcon fontSize='small'/>,
    'cloudy': <WbCloudyIcon fontSize='small'/>,
    'overcast': <FilterDramaIcon fontSize='small'/>,
    'drizzle': <WaterDropIcon fontSize='small'/>,
    'light-rain': <WaterDropIcon fontSize='small'/>,
    'rain': <WaterDropIcon fontSize='small'/>,
    'moderate-rain': <WaterDropIcon fontSize='small'/>,
    'heavy-rain': <WaterDropIcon fontSize='small'/>,
    'continuous-heavy-rain': <WaterDropIcon fontSize='small'/>,
    'showers': <WaterDropIcon fontSize='small'/>,
    'wet-snow': <WaterDropIcon fontSize='small'/>,
    'light-snow': <AcUnitIcon fontSize='small'/>,
    'snow': <AirIcon fontSize='small'/>,
    'snow-showers': <WaterDropIcon fontSize='small'/>,
    'hail': <WaterDropIcon fontSize='small'/>,
    'thunderstorm': <ThunderstormIcon fontSize='small'/>,
    'thunderstorm-with-rain': <ThunderstormIcon fontSize='small'/>,
    'thunderstorm-with-hail': <ThunderstormIcon fontSize='small'/>
}