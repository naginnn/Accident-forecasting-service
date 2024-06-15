import {FC} from "react";

import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import {orange, red} from "@mui/material/colors";
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";
import {TableCell, Typography} from "@mui/material";

import {VisibleColumnT} from "@src/widgets/tableFilter";
import {FocusedTableRow} from "@src/shared/ui/focusedTableRow";
import {CopyCell} from "@src/entities/copyCell";

import {FormattedConsumer, CriticalStatusName} from "../../types/formattedConsumer";

interface IConsumerRowProps {
    info: FormattedConsumer
    visibleColumn: VisibleColumnT<FormattedConsumer>
    setActiveConsumer: React.Dispatch<React.SetStateAction<FormattedConsumer | undefined>>
}

export const ConsumerRow: FC<IConsumerRowProps> = ({info, visibleColumn, setActiveConsumer}) => {
    const getCell = (
        info: FormattedConsumer,
        keyName: Extract<
            keyof FormattedConsumer,
            'address' | 'balance_holder' | 'sock_type' | 'total_area' | 'floors'
            | 'is_dispatch' | 'energy_class' | 'operating_mode'
            | 'priority' | 'target'
        >,
        isCopy: boolean = false
    ) => {
        if (visibleColumn && visibleColumn[keyName]) {
            let val = info[keyName]

            if (typeof val === 'boolean')
                val = val ? 'Да' : 'Нет'

            return isCopy
                ? <CopyCell>
                    {info[keyName]}
                </CopyCell>
                : <TableCell>
                <Typography variant='body2'>
                    {val}
                </Typography>
            </TableCell>
        }

        return null
    }

    const getStatusCell = (keyName: 'critical_status') => {
        if (visibleColumn && visibleColumn[keyName]) {
            if (info.critical_status === CriticalStatusName.IS_WARNING) {
                return <TableCell>
                    <WarningAmberIcon sx={{color: orange[600]}}/>
                </TableCell>
            } else if (info.critical_status === CriticalStatusName.IS_APPROVED) {
                return <TableCell>
                    <ErrorOutlineIcon sx={{color: red[700]}}/>
                </TableCell>
            }

            return <TableCell/>
        }

        return null
    }


    return (
        <FocusedTableRow onClick={() => setActiveConsumer(info)}>
            {getStatusCell('critical_status')}
            {getCell(info, 'address', true)}
            {getCell(info, 'balance_holder')}
            {getCell(info, 'sock_type')}
            {getCell(info, 'target')}
            {getCell(info, 'total_area')}
            {getCell(info, 'floors')}
            {getCell(info, 'is_dispatch')}
            {getCell(info, 'energy_class')}
            {getCell(info, 'operating_mode')}
            {getCell(info, 'priority')}
        </FocusedTableRow>
    )
}

