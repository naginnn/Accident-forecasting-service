//@ts-nocheck
import {FC, useMemo} from "react";

import {TableBody} from "@mui/material";

import {TableFilter, VisibleColumnT} from "@src/widgets/tableFilter";
import {sortArr} from "@src/shared/lib/sortArr";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {DownloadExcelButton} from "@src/shared/ui/downloadExlsBtn";

import {ConsumerRow} from "./ConsumerRow";
import {FormattedConsumer} from "../../types/formattedConsumer";
import {useDownloadConsumerStation} from "../../api/downloadExcel";

interface ConsumersTableProps {
    data: FormattedConsumer[]
    consumerStationId: number | undefined
    setActiveConsumer: React.Dispatch<React.SetStateAction<FormattedConsumer | undefined>>
}

export const ConsumersTable: FC<ConsumersTableProps> = ({data, setActiveConsumer, consumerStationId}) => {
    const {downloadExcel, error} = useDownloadConsumerStation()
    const sortedData: FormattedConsumer[] = useMemo(() => {
        return sortArr(data, 'priority', 'desc', true)
    }, [data])


    const getTableBodyLayout = (data: FormattedConsumer[], getPageContent: (x: FormattedConsumer[]) => FormattedConsumer[], visibleColumn: VisibleColumnT<FormattedConsumer>) => {
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
        <ErrorWrapper
            snackBarErrors={{
                errors: [{error, message: 'Не удалось загрузить excel'}]
            }}
        >
            <TableFilter
                data={sortedData}
                getTableBodyLayout={getTableBodyLayout}
                withPagination
            >
                <TableFilter.Banner withSearch withManageColumn>
                    {
                        typeof consumerStationId !== 'undefined' &&
                        <DownloadExcelButton onClick={() => downloadExcel(consumerStationId)}>
                            Загрузить excel
                        </DownloadExcelButton>
                    }
                </TableFilter.Banner>
                <TableFilter.SelectCell
                    isInvisible
                    keyName='critical_status'
                    id='critical_status'
                    sx={{width: '50px'}}
                    topic='Статус критичности'
                />
                <TableFilter.SelectCell keyName='address' id='address' topic='Адрес' sx={{width: '230px'}}/>
                <TableFilter.SelectCell keyName='balance_holder' id='balance_holder' topic='Балансодержатель'/>
                <TableFilter.SelectCell keyName='sock_type' id='sock_type' topic='Тип'/>
                <TableFilter.SelectCell keyName='target' id='target' topic='Назначение'/>
                <TableFilter.SortCell keyName='total_area' id='total_area' topic='Общ. площадь'/>
                <TableFilter.SortCell keyName='floors' id='floors' topic='Кол-во этажей'/>
                <TableFilter.SelectCell booleanName={['Да', 'Нет']} keyName='is_dispatch' id='is_dispatch'
                                        topic='Диспетчеризация'/>
                <TableFilter.SelectCell keyName='energy_class' id='energy_class' topic='Класс энергоэффективности'/>
                <TableFilter.SelectCell keyName='operating_mode' id='operating_mode' topic='Время работы'/>
                <TableFilter.SortCell keyName='priority' id='priority' topic='Приоритет'/>
            </TableFilter>
        </ErrorWrapper>
    )
};
