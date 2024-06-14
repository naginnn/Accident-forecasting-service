import cls from './clusterLayer.module.scss'
import {FC} from "react";
import {LngLat} from "ymaps3";
import {useNavigate} from "react-router-dom";

import {IconButton, Typography} from '@mui/material';
import CloseIcon from "@mui/icons-material/Close";

import {YMapMarker} from "@src/widgets/YMap";
import {useToggle} from "@src/shared/hooks/useToggle";
import {classNames} from "@src/shared/lib/classNames";
import {CriticalStatusName} from "@src/pages/consumers/api/getConsumers";
import {PaperWrapper} from '@src/shared/ui/paperWrapper';
import {openNewWindowPage} from "@src/shared/lib/openNewWindowPage";

import {TransformConsumers} from "../../api/getConsumers";
import { Link } from '@src/shared/ui/link';

interface PopupMarkerProps {
    coordinates: LngLat
    info: TransformConsumers
}

export const PopupMarker: FC<PopupMarkerProps> = ({coordinates, info}) => {
    const {on: openPopup, off: closePopup, value: isOpenPopup} = useToggle()
    const navigate = useNavigate()

    const onOpenConsumerCortnsPage = () => {
        const url = '/consumers/' + info.consumer_station_id
        navigate(url);
    }

    const onOpenConsumerCortnsNewPage = (e: React.MouseEvent<HTMLTableRowElement, MouseEvent>) => {
        const url = '/consumers/' + info.consumer_station_id
        if (e.button === 1) {
            openNewWindowPage(url)
        }
    }

    return (
        <>
            <YMapMarker coordinates={coordinates} source="clusterer-source" zIndex={1800}>
                <div
                    onClick={openPopup}
                    className={classNames(
                        cls.pin,
                        {
                            [cls.pin_red]: info.critical_status === CriticalStatusName.IS_APPROVED,
                            [cls.pin_orange]: info.critical_status === CriticalStatusName.IS_WARNING
                        }
                    )}
                />
                <div className={
                    classNames(
                        cls.pulse,
                        {
                            [cls.pulse_red]: info.critical_status === CriticalStatusName.IS_APPROVED,
                            [cls.pulse_orange]: info.critical_status === CriticalStatusName.IS_WARNING
                        }
                    )
                }/>
            </YMapMarker>
            {
                isOpenPopup &&
                <YMapMarker
                    source="clusterer-source"
                    coordinates={coordinates}
                    blockBehaviors
                    zIndex={2000}
                >
                    <PaperWrapper sx={{maxHeight: '500px', position: 'relative', minWidth: '300px', width: 'max-content'}}>
                        <IconButton
                            sx={{ml: 'auto', display: 'block', height: '40px'}}
                            onClick={closePopup}
                        >
                            <CloseIcon/>
                        </IconButton>
                        <Typography>
                            <b>Адрес потребителя:</b>
                            &nbsp;
                            <Link
                                onClick={onOpenConsumerCortnsPage}
                                onMouseDown={onOpenConsumerCortnsNewPage}
                            >
                                {info.consumer_address}
                            </Link>
                        </Typography>
                        <Typography>
                            <b>Тип потребителя:</b>
                            &nbsp;
                            {info.consumer_name}
                        </Typography>
                        <Typography>
                            <b>Округ:</b>
                            &nbsp;
                            {info.location_district_consumer_name}
                        </Typography>
                        <Typography>
                            <b>Район:</b>
                            &nbsp;
                            {info.location_area_consumer_name}
                        </Typography>
                        <Typography>
                            <b>Имя источника:</b>
                            &nbsp;
                            {info.source_station_name}
                        </Typography>
                        <Typography>
                            <b>Адрес источника:</b>
                            &nbsp;
                            {info.source_station_address}
                        </Typography>
                        <Typography>
                            <b>Имя ЦТП:</b>
                            &nbsp;
                            {info.consumer_station_name}
                        </Typography>
                        <Typography>
                            <b>Адрес ЦТП:</b>
                            &nbsp;
                            {info.consumer_station_address}
                        </Typography>
                        <Typography>
                            <b>Вероятность предсказания:</b>
                            &nbsp;
                            {info.probability}
                        </Typography>
                    </PaperWrapper>
                </YMapMarker>
            }
        </>
    );
};
