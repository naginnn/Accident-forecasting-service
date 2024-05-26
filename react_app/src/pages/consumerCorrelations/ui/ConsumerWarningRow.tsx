import {FC} from "react";

import {VisibleColumnT} from "@src/widgets/tableFilter";

import {TableCell, Typography} from "@mui/material";
import TableRow from "@mui/material/TableRow";

import {Consumer} from "../types/consumerCorrelationsInfo";

interface IConsumerWarningRowProps {
    info: Consumer
    visibleColumn: VisibleColumnT<Consumer>
}

export const ConsumerWarningRow: FC<IConsumerWarningRowProps> = ({info, visibleColumn}) => {
    const getCell = (
        info: Consumer,
        keyName: Extract<
            keyof Consumer,
            'name' | 'address' | 'total_area' | 'living_area'
            | 'energy_class' | 'operating_mode' | 'priority'
        >
    ) => {
        if (visibleColumn && visibleColumn[keyName]) {
            return <TableCell>
                <Typography variant='body2'>
                    {info[keyName]}
                </Typography>
            </TableCell>
        }

        return null
    }

    return (
        <TableRow>
            {getCell(info, 'name')}
            {getCell(info, 'address')}
            {getCell(info, 'total_area')}
            {getCell(info, 'living_area')}
            {getCell(info, 'energy_class')}
            {getCell(info, 'operating_mode')}
            {getCell(info, 'priority')}
        </TableRow>
    )
}

