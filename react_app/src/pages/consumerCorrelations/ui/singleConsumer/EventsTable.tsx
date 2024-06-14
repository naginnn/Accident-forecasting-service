//@ts-nocheck
import {FC, useMemo} from "react";

import {Box, Typography} from "@mui/material";

import {CollapsedBlock} from "@src/entities/collapsedBlock";
import {TableFilter} from "@src/widgets/tableFilter";
import {transformDateFormat} from "@src/shared/lib/transformDateFormat";

import {EventConsumer} from "../../types/consumerCorrelationsInfo";

interface EventsTableProps {
    data: EventConsumer[] | null
}

export const EventsTable: FC<EventsTableProps> = ({data}) => {
    const fomattedData = useMemo(() => {
        return data.map(el => {
            return {
                ...el,
                created: transformDateFormat(el.created, 'DD/MM/YYYY'),
                closed: transformDateFormat(el.closed, 'DD/MM/YYYY')
            }
        })
    }, [data])

    return (
        <Box sx={{mt: '16px'}}>
            <CollapsedBlock topicName='Инциденты на потребителях'>
                {
                    data?.length
                        ? <TableFilter
                            data={fomattedData}
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
            </CollapsedBlock>
        </Box>
    );
};
