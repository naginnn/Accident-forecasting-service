import {FC} from "react";

import HolidayVillageIcon from '@mui/icons-material/HolidayVillage';
import CloseIcon from '@mui/icons-material/Close';
import {IconButton, Paper, Typography} from "@mui/material";

import {useToggle} from "@src/shared/hooks/useToggle";
import {YMapMarker} from "@src/widgets/YMap";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {ConsumerStations} from "../../types/consumerCorrelationsInfo";

interface ConsumerStationLayerProps {
    info: ConsumerStations
}

export const ConsumerStationPopup: FC<ConsumerStationLayerProps> = ({info}) => {
    const {on: openPopup, off: closePopup, value: isOpenPopup} = useToggle()

    return (
        <>
            <YMapMarker coordinates={info.geo_data.center}>
                <Paper sx={{p: '4px', cursor: 'pointer', color: '#039be5'}} onClick={openPopup}>
                    <HolidayVillageIcon/>
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
                            <b>Адрес:</b>
                            &nbsp;
                            {info.address}
                        </Typography>
                        <Typography>
                            <b>Имя:</b>
                            &nbsp;
                            {info.name}
                        </Typography>
                        <Typography>
                            <b>Тип:</b>
                            &nbsp;
                            {info.type}
                        </Typography>
                        <Typography>
                            <b>Расположение:</b>
                            &nbsp;
                            {info.place_type}
                        </Typography>
                        <Typography>
                            <b>Адрес ОДС:</b>
                            &nbsp;
                            {info.ods_address}
                        </Typography>
                        <Typography>
                            <b>Имя ОДС:</b>
                            &nbsp;
                            {info.ods_name}
                        </Typography>
                        <Typography>
                            <b>Потребитель или УК:</b>
                            &nbsp;
                            {info.ods_manager_company}
                        </Typography>
                    </PaperWrapper>
                </YMapMarker>
            }
        </>
    );
};
