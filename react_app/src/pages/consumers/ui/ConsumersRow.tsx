import {FC} from "react";
import {useNavigate} from "react-router-dom";

import {orange, red} from "@mui/material/colors";

import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";

import {TableCell, Typography} from "@mui/material";

import {FocusedTableRow} from "@src/shared/ui/focusedTableRow";
import {VisibleColumnT} from "@src/widgets/tableFilter";

import {CriticalStatusName, TransformConsumers} from "../api/getConsumers";
import {EditStatusButton} from "./EditStatusButton";
import {openNewWindowPage} from "@src/shared/lib/openNewWindowPage";

interface IConsumersProps {
    info: TransformConsumers
    visibleColumn: VisibleColumnT<TransformConsumers>
    updateStatus: React.Dispatch<React.SetStateAction<TransformConsumers[]>>
    criticalStatus: CriticalStatusName
}

export const ConsumersRow: FC<IConsumersProps> = ({info, visibleColumn, updateStatus, criticalStatus}) => {
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

    const getCell = (info: TransformConsumers, keyName: keyof TransformConsumers) => {
        if (visibleColumn && visibleColumn[keyName]) {
            return <TableCell>
                <Typography variant='body2'>
                    {info[keyName]}
                </Typography>
            </TableCell>
        }
        return null
    }

    const getStatusCell = () => {
        if (criticalStatus === CriticalStatusName.IS_WARNING) {
            return <TableCell>
                <WarningAmberIcon sx={{color: orange[600]}}/>
            </TableCell>
        } else if (criticalStatus === CriticalStatusName.IS_APPROVED) {
            return <TableCell>
                <ErrorOutlineIcon sx={{color: red[700]}}/>
            </TableCell>
        }

        return <TableCell/>
    }

    return (
        <FocusedTableRow
            onClick={onOpenConsumerCortnsPage}
            onMouseDown={onOpenConsumerCortnsNewPage}
        >
            {getStatusCell()}
            {getCell(info, 'consumer_address')}
            {getCell(info, 'consumer_name')}
            {getCell(info, 'location_district_consumer_name')}
            {getCell(info, 'location_area_consumer_name')}
            {getCell(info, 'source_station_name')}
            {getCell(info, 'source_station_address')}
            {getCell(info, 'consumer_station_name')}
            {getCell(info, 'consumer_station_address')}
            {getCell(info, 'probability')}
            <TableCell>
                <EditStatusButton
                    info={info}
                    updateStatus={updateStatus}
                />
            </TableCell>
        </FocusedTableRow>
    )
}

