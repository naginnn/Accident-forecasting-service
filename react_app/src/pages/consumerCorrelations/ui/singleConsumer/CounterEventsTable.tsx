//@ts-nocheck
import {FC} from "react";

import {Typography} from "@mui/material";

import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {TableFilter} from "@src/widgets/tableFilter";

import {useGetCounterEventsQuery} from "../../api/getEventsCounter";

interface CounterEventsTableProps {
    consumerId: number
}

export const CounterEventsTable: FC<CounterEventsTableProps> = ({consumerId}) => {
    const {data, error, isLoading} = useGetCounterEventsQuery(consumerId)

    return (
        <LoadingWrapper
            isLoading={isLoading}
            displayType='linear'
        >
            <ErrorWrapper
                snackBarErrors={{
                    errors: [{error, message: 'Не удалось загрузить выгрузку ОДПУ отопления'}],
                    blockContent: true
                }}
            >
                {
                    data?.length
                        ? <TableFilter
                            data={data}
                            withPagination
                        >
                            <TableFilter.Banner withSearch/>
                            <TableFilter.SelectCell keyName='counter_number' id='counter_number' topic='Номер счетчика'/>
                            <TableFilter.SelectCell keyName='contour' id='contour' topic='Контур'/>
                            <TableFilter.SelectCell keyName='counter_mark' id='counter_mark' topic='Марка счетчика'/>
                            <TableFilter.SortCell keyName='gcal_in_system' id='gcal_in_system' topic='Объём поданого теплоносителя'/>
                            <TableFilter.SortCell keyName='gcal_out_system' id='gcal_out_system' topic='Объём обратного теплоносителя'/>
                            <TableFilter.SortCell keyName='subset' id='subset' topic='Подмес'/>
                            <TableFilter.SortCell keyName='leak' id='leak' topic='Утечка'/>
                            <TableFilter.SortCell keyName='supply_temp' id='supply_temp' topic='Температура подачи'/>
                            <TableFilter.SortCell keyName='return_temp' id='return_temp' topic='Температура обратки'/>
                            <TableFilter.SortCell keyName='work_hours_counter' id='work_hours_counter' topic='Наработка часов счётчика'/>
                            <TableFilter.SortCell keyName='heat_thermal_energy' id='heat_thermal_energy' topic='Расход тепловой энергии'/>
                            <TableFilter.SortCell keyName='errors' id='errors' topic='Ошибки'/>
                        </TableFilter>
                        : <Typography>Данные отсутствуют</Typography>
                }
            </ErrorWrapper>
        </LoadingWrapper>

    );
};
