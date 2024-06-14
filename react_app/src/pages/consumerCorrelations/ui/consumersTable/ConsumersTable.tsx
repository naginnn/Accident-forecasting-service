//@ts-nocheck
import {FC, useMemo} from "react";

import {TableBody} from "@mui/material";

import {TableFilter, VisibleColumnT} from "@src/widgets/tableFilter";
import {sortArr} from "@src/shared/lib/sortArr";

import {Consumer} from "../../types/consumerCorrelationsInfo";
import {ConsumerRow} from "./ConsumerRow";

interface ConsumersTableProps {
    data: Consumer[]
    setActiveConsumer: React.Dispatch<React.SetStateAction<Consumer | undefined>>
}

export const ConsumersTable: FC<ConsumersTableProps> = ({data, setActiveConsumer}) => {
    const sortedData = useMemo(() => {
        return sortArr(data, 'priority', 'desc', true)
    }, [data])


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
                data={sortedData}
                getTableBodyLayout={getTableBodyLayout}
                withPagination
            >
                <TableFilter.Banner withSearch withManageColumn/>
                <TableFilter.SelectCell keyName='address' id='address' topic='Адрес' sx={{width: '15%'}}/>
                <TableFilter.SelectCell keyName='balance_holder' id='balance_holder' topic='Балансодержатель'/>
                <TableFilter.SelectCell keyName='sock_type' id='sock_type' topic='Тип'/>
                <TableFilter.SortCell keyName='total_area' id='total_area' topic='Общ. площадь'/>
                <TableFilter.SortCell keyName='floors' id='floors' topic='Кол-во этажей'/>
                <TableFilter.SelectCell booleanName={['Да', 'Нет']} keyName='is_dispatch' id='is_dispatch' topic='Диспетчеризация'/>
                <TableFilter.SelectCell keyName='energy_class' id='energy_class' topic='Класс энергоэффективности'/>
                <TableFilter.SelectCell keyName='operating_mode' id='operating_mode' topic='Время работы'/>
                <TableFilter.SortCell keyName='priority' id='priority' topic='Приоритет'/>
            </TableFilter>
    )
};
