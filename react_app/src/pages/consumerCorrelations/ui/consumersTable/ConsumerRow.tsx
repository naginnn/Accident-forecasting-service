import {FC} from "react";

import {VisibleColumnT} from "@src/widgets/tableFilter";
import {FocusedTableRow} from "@src/shared/ui/focusedTableRow";

import {TableCell, Typography} from "@mui/material";

import {Consumer} from "../../types/consumerCorrelationsInfo";

interface IConsumerRowProps {
    info: Consumer
    visibleColumn: VisibleColumnT<Consumer>
    setActiveConsumer: React.Dispatch<React.SetStateAction<Consumer | undefined>>
}

export const ConsumerRow: FC<IConsumerRowProps> = ({info, visibleColumn, setActiveConsumer}) => {
    const getCell = (
        info: Consumer,
        keyName: Extract<
            keyof Consumer,
            'address' | 'balance_holder' | 'sock_type' | 'total_area' | 'floors'
            | 'is_dispatch' | 'energy_class' | 'operating_mode'
            | 'priority'
        >
    ) => {
        if (visibleColumn && visibleColumn[keyName]) {
            let val = info[keyName]

            if (typeof val === 'boolean')
                val = val ? 'Да' : 'Нет'

            return <TableCell onClick={() => setActiveConsumer(info)}>
                <Typography variant='body2'>
                    {val}
                </Typography>
            </TableCell>
        }

        return null
    }


    return (
        <FocusedTableRow>
            {getCell(info, 'address')}
            {getCell(info, 'balance_holder')}
            {getCell(info, 'sock_type')}
            {getCell(info, 'total_area')}
            {getCell(info, 'floors')}
            {getCell(info, 'is_dispatch')}
            {getCell(info, 'energy_class')}
            {getCell(info, 'operating_mode')}
            {getCell(info, 'priority')}
        </FocusedTableRow>
    )
}

