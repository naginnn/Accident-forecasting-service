import {FC} from "react";

import FactoryIcon from '@mui/icons-material/Factory';
import {Box, Divider, List, ListItem, ListItemAvatar, ListItemText, Typography} from "@mui/material";

import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {SourceStations} from "../types/consumerCorrelationsInfo";

interface SourceStationBlockProps {
    info: SourceStations
}

export const SourceStationBlock: FC<SourceStationBlockProps> = ({info}) => {
    return (
        <PaperWrapper sx={{position: 'relative', mt: 0, height: '100%'}}>
            <Typography variant='h5' gutterBottom>
                Источники тепла
            </Typography>
            <Divider/>
            <Box sx={{mt: '8px', display: 'flex', alignItems: 'end', gap: '8px'}}>
                <FactoryIcon sx={{color: '#f57f17'}}/>
                <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                    {info.name}
                </Typography>
            </Box>
            <Typography gutterBottom component='div' sx={{mt: '8px'}}>
                <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                    Адрес:&nbsp;
                </Typography>
                {info.address}
            </Typography>
            <Typography gutterBottom component='div'>
                <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                    Кол-во котлов:&nbsp;
                </Typography>
                {info.boiler_count}
            </Typography>
            <Typography gutterBottom component='div'>
                <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                    Тепловая мощность:&nbsp;
                </Typography>
                {info.t_power}
            </Typography>
            <Typography gutterBottom component='div'>
                <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                    Кол-во турбин:&nbsp;
                </Typography>
                {info.turbine_count}
            </Typography>
            <Typography gutterBottom component='div'>
                <Typography sx={{display: 'inline-block', fontWeight: 500}}>
                    Электрическая мощность:&nbsp;
                </Typography>
                {info.e_power}
            </Typography>
        </PaperWrapper>
)
}
