import {FC} from "react";

import {VisibleColumnT} from "@src/widgets/tableFilter";
import {FocusedTableRow} from "@src/shared/ui/focusedTableRow";

import {TableCell, Typography} from "@mui/material";

import {Consumer} from "../types/consumerCorrelationsInfo";

interface IConsumerRowProps {
    info: Consumer
    visibleColumn: VisibleColumnT<Consumer>
    setActiveConsumer: React.Dispatch<React.SetStateAction<number | undefined>>
}

export const ConsumerRow: FC<IConsumerRowProps> = ({info, visibleColumn, setActiveConsumer}) => {
    const getCell = (
        info: Consumer,
        keyName: Extract<
            keyof Consumer,
            'name' | 'address' | 'total_area' | 'living_area'
            | 'energy_class' | 'operating_mode' | 'priority'
        >
    ) => {
        if (visibleColumn && visibleColumn[keyName]) {
            return <TableCell onClick={() => setActiveConsumer(info.id)}>
                <Typography variant='body2'>
                    {info[keyName]}
                </Typography>
            </TableCell>
        }

        return null
    }

    return (
        <FocusedTableRow>
            {getCell(info, 'name')}
            {getCell(info, 'address')}
            {getCell(info, 'total_area')}
            {getCell(info, 'living_area')}
            {getCell(info, 'energy_class')}
            {getCell(info, 'operating_mode')}
            {getCell(info, 'priority')}
        </FocusedTableRow>
    )
}

