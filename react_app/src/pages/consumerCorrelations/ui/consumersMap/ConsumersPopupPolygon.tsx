import {FC} from "react";

import {IconButton, Typography} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import {orange, red} from "@mui/material/colors";

import {YMapMarker, YMapFeature} from "@src/widgets/YMap";
import {useToggle} from "@src/shared/hooks/useToggle";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";
import {Link} from "@src/shared/ui/link";

import {Consumer} from "../../types/consumerCorrelationsInfo";

interface ConsumersPopupPolygonProps {
    info: Consumer
    setActiveConsumer: React.Dispatch<React.SetStateAction<Consumer | undefined>>
}

export const ConsumersPopupPolygon: FC<ConsumersPopupPolygonProps> = ({info, setActiveConsumer}) => {
    const {on: openPopup, off: closePopup, value: isOpenPopup} = useToggle()

    const getPolygonColor = () => {
        if (info.events?.length && !info.events[0].is_closed) {
            if (info.events[0].is_approved) {
                return red[500]
            } else {
                return orange[500]
            }
        }

        return '#006efc'
    }

    const fillPolygonColor = () => {
        if (info.events?.length && !info.events[0].is_closed) {
            if (info.events[0].is_approved) {
                return red[100]
            } else {
                return orange[100]
            }
        }

        return 'rgba(56, 56, 219, 0.5)'
    }

    return (
        <>
            <YMapMarker coordinates={info.geo_data.center}>
                <YMapFeature
                    onClick={openPopup}
                    geometry={{
                        type: 'Polygon',
                        coordinates: [info.geo_data.polygon]
                    }}
                    style={{
                        cursor: 'pointer',
                        stroke: [{
                            color: getPolygonColor(),
                            width: 2
                        }],
                        fill: fillPolygonColor()
                    }}
                />
            </YMapMarker>
            {
                isOpenPopup &&
                <YMapMarker
                    coordinates={info.geo_data.center}
                    zIndex={1000}
                    blockBehaviors
                >
                    <PaperWrapper sx={{maxHeight: '500px', position: 'relative', width: 'max-content', minWidth: '300px'}}>
                        <IconButton
                            sx={{ml: 'auto', display: 'block', height: '40px'}}
                            onClick={closePopup}
                        >
                            <CloseIcon/>
                        </IconButton>
                        <Typography>
                            <b>Адрес:</b>
                            &nbsp;
                            <Link onClick={() => setActiveConsumer(info)}>
                                {info.address || '-'}
                            </Link>
                        </Typography>
                        <Typography>
                            <b>Балансодержатель:</b>
                            &nbsp;
                            {info.balance_holder || '-'}
                        </Typography>
                        <Typography>
                            <b>Тип:</b>
                            &nbsp;
                            {info.sock_type || '-'}
                        </Typography>
                        <Typography>
                            <b>Общ. площадь:</b>
                            &nbsp;
                            {info.total_area || '-'}
                        </Typography>
                        <Typography>
                            <b>Кол-во этажей:</b>
                            &nbsp;
                            {info.floors || '-'}
                        </Typography>
                        <Typography>
                            <b>Диспетчеризация:</b>
                            &nbsp;
                            {info.is_dispatch ? 'Да' : 'Нет'}
                        </Typography>
                        <Typography>
                            <b>Класс энергоэффективности:</b>
                            &nbsp;
                            {info.energy_class || '-'}
                        </Typography>
                        <Typography>
                            <b>Время работы:</b>
                            &nbsp;
                            {info.operating_mode || '-'}
                        </Typography>
                        <Typography>
                            <b>Приоритет:</b>
                            &nbsp;
                            {info.priority || '-'}
                        </Typography>
                    </PaperWrapper>
                </YMapMarker>
            }
        </>

    );
};
