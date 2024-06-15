import {FC} from "react";
import {useNavigate} from "react-router-dom";

import {orange, red} from "@mui/material/colors";

import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";

import {TableCell, Typography} from "@mui/material";

import {FocusedTableRow} from "@src/shared/ui/focusedTableRow";
import {VisibleColumnT} from "@src/widgets/tableFilter";
import {openNewWindowPage} from "@src/shared/lib/openNewWindowPage";

import {CriticalStatusName, TransformConsumers} from "../../api/getConsumers";
import {EditStatusButton} from "./EditStatusButton";
import {CopyCell} from "@src/entities/copyCell";

interface IConsumersProps {
    info: TransformConsumers
    visibleColumn: VisibleColumnT<TransformConsumers> & { manage_table: boolean }
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

    const getCell = (info: TransformConsumers, keyName: Exclude<keyof TransformConsumers, 'consumer_geo_data' | 'critical_status'>, isCopy: boolean = false) => {
        if (visibleColumn && visibleColumn[keyName]) {
            return isCopy
                ? <CopyCell>
                    {info[keyName]}
                </CopyCell>
                : <TableCell>
                    <Typography variant='body2'>
                        {info[keyName]}
                    </Typography>
                </TableCell>
        }
        return null
    }

    const getStatusCell = (keyName: keyof TransformConsumers) => {
        if (visibleColumn && visibleColumn[keyName]) {
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

        return null
    }

    const getEditButtonCell = () => {
        if (visibleColumn && visibleColumn['manage_table']) {
            return <TableCell>
                <EditStatusButton
                    info={info}
                    updateStatus={updateStatus}
                />
            </TableCell>
        }
        return null
    }

    return (
        <FocusedTableRow
            onClick={onOpenConsumerCortnsPage}
            onMouseDown={onOpenConsumerCortnsNewPage}
        >
            {getStatusCell('critical_status')}
            {getCell(info, 'consumer_address', true)}
            {getCell(info, 'location_district_consumer_name')}
            {getCell(info, 'location_area_consumer_name')}
            {getCell(info, 'source_station_name')}
            {getCell(info, 'source_station_address')}
            {getCell(info, 'consumer_station_name')}
            {getCell(info, 'consumer_station_address')}
            {getCell(info, 'probability')}
            {getEditButtonCell()}
        </FocusedTableRow>
    )
}

