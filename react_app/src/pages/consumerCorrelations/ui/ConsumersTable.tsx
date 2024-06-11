//@ts-nocheck
import {FC} from "react";

import {TableBody} from "@mui/material";

import {TableFilter, VisibleColumnT} from "@src/widgets/tableFilter";

import {Consumer} from "../types/consumerCorrelationsInfo";
import {ConsumerRow} from "./ConsumerRow";

interface ConsumersTableProps {
    data: Consumer[]
    setActiveConsumer: React.Dispatch<React.SetStateAction<number | undefined>>
}

export const ConsumersTable: FC<ConsumersTableProps> = ({data, setActiveConsumer}) => {
    const getTableBodyLayout = (data: Consumer[], getPageContent: (x: Consumer[]) => Consumer[], visibleColumn: VisibleColumnT<Consumer>) => {
        return (
            <TableBody>
                {
                    getPageContent(data).map(row => {
                        return (
                            <ConsumerRow
                                key={row.id}
                                info={row}
                                visibleColumn={visibleColumn}
                                setActiveConsumer={setActiveConsumer}
                            />
                        )
                    })
                }
            </TableBody>
        )
    }


    return (
            <TableFilter
                data={data}
                getTableBodyLayout={getTableBodyLayout}
                withPagination
            >
                <TableFilter.Banner withSearch withManageColumn/>
                <TableFilter.SelectCell keyName='name' id='name' topic='Тип'/>
                <TableFilter.Cell keyName='address' id='address' topic='Адрес'/>
                <TableFilter.SortCell keyName='total_area' id='total_area' topic='Общ. площадь'/>
                <TableFilter.SortCell keyName='living_area' id='living_area' topic='Жил. площадь'/>
                <TableFilter.SelectCell keyName='energy_class' id='energy_class' topic='Класс энергоэффективности'/>
                <TableFilter.SelectCell keyName='operating_mode' id='operating_mode' topic='Время работы'/>
                <TableFilter.SortCell keyName='priority' id='priority' topic='Приоритет'/>
            </TableFilter>
    )
};
