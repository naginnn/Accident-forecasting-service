import {FC} from "react";

import FactoryIcon from '@mui/icons-material/Factory';
import CloseIcon from '@mui/icons-material/Close';
import {IconButton, Paper, Typography} from "@mui/material";

import {useToggle} from "@src/shared/hooks/useToggle";
import {YMapMarker} from "@src/widgets/YMap";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {SourceStations} from "../../types/consumerCorrelationsInfo";

interface SourcetationLayerProps {
    info: SourceStations
}

export const SourceStationPopup: FC<SourcetationLayerProps> = ({info}) => {
    const {on: openPopup, off: closePopup, value: isOpenPopup} = useToggle()

    return (
        <>
            <YMapMarker coordinates={info.geo_data.center}>
                <Paper sx={{p: '4px', cursor: 'pointer', color: '#f57f17'}} onClick={openPopup}>
                    <FactoryIcon/>
                </Paper>
            </YMapMarker>
            {
                isOpenPopup &&
                <YMapMarker
                    coordinates={info.geo_data.center}
                    zIndex={1900}
                    blockBehaviors
                >
                    <PaperWrapper
                        sx={{maxHeight: '500px', position: 'relative', minWidth: '300px', width: 'max-content'}}>
                        <IconButton
                            sx={{ml: 'auto', display: 'block', height: '40px'}}
                            onClick={closePopup}
                        >
                            <CloseIcon/>
                        </IconButton>
                        <Typography>
                            <b>Имя:</b>
                            &nbsp;
                            {info.name}
                        </Typography>
                        <Typography>
                            <b>Адрес:</b>
                            &nbsp;
                            {info.address}
                        </Typography>
                        <Typography>
                            <b>Кол-во котлов:</b>
                            &nbsp;
                            {info.boiler_count}
                        </Typography>
                        <Typography>
                            <b>Тепловая мощность:</b>
                            &nbsp;
                            {info.t_power} Гкал/ч
                        </Typography>
                        <Typography>
                            <b>Кол-во турбин:</b>
                            &nbsp;
                            {info.turbine_count}
                        </Typography>
                        <Typography>
                            <b>Электрическая мощность:</b>
                            &nbsp;
                            {info.e_power} МВт
                        </Typography>
                    </PaperWrapper>
                </YMapMarker>
            }
        </>
    );
};
