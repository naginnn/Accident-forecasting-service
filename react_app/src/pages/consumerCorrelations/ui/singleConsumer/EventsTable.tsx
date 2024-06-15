//@ts-nocheck
import {FC, useMemo} from "react";

import {Typography} from "@mui/material";

import {TableFilter} from "@src/widgets/tableFilter";
import {transformDateFormat} from "@src/shared/lib/transformDateFormat";
import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {sortArrOfObjByTime} from "@src/shared/lib/sortArrOfObjByTime";

import {useGetConsumerEventsQuery} from "../../api/getConsumerEvents";

interface EventsTableProps {
    consumerId: number
}

export const EventsTable: FC<EventsTableProps> = ({consumerId}) => {
    const {data, isLoading, error} = useGetConsumerEventsQuery(consumerId)

    const formattedData = useMemo(() => {
        if (!data)
            return null

        return sortArrOfObjByTime(data, 'created', 'desc').map(el => {
            const closedData = transformDateFormat(el.closed, 'DD/MM/YYYY')

            return {
                ...el,
                created: transformDateFormat(el.created, 'DD/MM/YYYY'),
                closed: closedData === '01/01/0001' ? '' : closedData
            }
        })
    }, [data])

    return (
        <LoadingWrapper isLoading={isLoading} displayType='linear'>
            <ErrorWrapper
                snackBarErrors={{
                    errors: [{error, message: 'Не удалось загрузить инциденты'}],
                    blockContent: true
                }}
            >
                {
                    formattedData?.length
                        ? <TableFilter
                            data={formattedData}
                            withPagination
                        >
                            <TableFilter.Banner withSearch/>
                            <TableFilter.SelectCell keyName='source' id='source' topic='Источник'/>
                            <TableFilter.SelectCell keyName='description' id='description' topic='Описание'/>
                            <TableFilter.SortCell keyName='probability' id='probability' topic='Вероятность'/>
                            <TableFilter.SortCell keyName='days_of_work' id='days_of_work' topic='Дней в работе'/>
                            <TableFilter.SortCell isDateCell keyName='created' id='created' topic='Дата открытия'/>
                            <TableFilter.SortCell isDateCell keyName='closed' id='closed' topic='Дата закрытия'/>
                        </TableFilter>
                        : <Typography>Данные отсутствуют</Typography>
                }
            </ErrorWrapper>
        </LoadingWrapper>
    );
};
