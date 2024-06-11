//@ts-nocheck
import {FC} from "react";

import {TableBody} from "@mui/material";

import {TransformConsumers} from "../api/getConsumers";

import {TableFilter, VisibleColumnT} from "@src/widgets/tableFilter";

import {ConsumersRow} from "./ConsumersRow";

interface ITableConsumersProps {
    data: TransformConsumers[]
    updateStatus: React.Dispatch<React.SetStateAction<TransformConsumers[]>>
}

export const TableConsumers: FC<ITableConsumersPropsZ> = ({data, updateStatus}) => {
    const getTableBodyLayout = (data: TransformConsumers[], getPageContent: (x: TransformConsumers[]) => TransformConsumers[], visibleColumn: VisibleColumnT<TransformConsumers>) => {
        return (
            <TableBody>
                {
                    getPageContent(data).map(row => {
                        return (
                            <ConsumersRow
                                key={row.consumer_id}
                                info={row}
                                criticalStatus={row.critical_status}
                                visibleColumn={visibleColumn}
                                updateStatus={updateStatus}
                            />
                        )
                    })
                }
            </TableBody>
        )
    }

    return (
        <TableFilter
            id='table_view'
            data={data}
            getTableBodyLayout={getTableBodyLayout}
            withPagination
        >
            <TableFilter.Banner withSearch withManageColumn/>
            <TableFilter.SelectCell
                isInvisible
                keyName='critical_status'
                id='critical_status'
                sx={{width: '50px'}}
                topic='Статус критичности'
            />
            <TableFilter.Cell
                keyName='consumer_address'
                id='consumer_address'
                topic='Адрес потребителя'
            />
            <TableFilter.SelectCell
                keyName='consumer_name'
                id='consumer_name'
                topic='Тип потребителя'
            />
            <TableFilter.SelectCell
                keyName='location_district_consumer_name'
                id='location_district_consumer_name'
                topic='Округ'
            />
            <TableFilter.SelectCell
                keyName='location_area_consumer_name'
                id='location_area_consumer_name'
                topic='Район'
            />
            <TableFilter.SelectCell
                keyName='source_station_name'
                id='source_station_name'
                topic='Имя источника'
            />
            <TableFilter.Cell
                keyName='source_station_address'
                id='source_station_address'
                topic='Адрес источника'
            />
            <TableFilter.SelectCell
                keyName='consumer_station_name'
                id='consumer_station_name'
                topic='Имя ЦТП'
            />
            <TableFilter.Cell
                keyName='consumer_station_address'
                id='consumer_station_address'
                topic='Адрес ЦТП'
            />

            <TableFilter.SortCell
                keyName='probability'
                id='probability'
                topic='Вероятность предсказания'
            />
            <TableFilter.Cell
                isInvisible
                keyName='manage_table'
                id='manage_table'
                sx={{width: '50px'}}
                topic='Управление инцидентом'
            />
        </TableFilter>

    );
}
