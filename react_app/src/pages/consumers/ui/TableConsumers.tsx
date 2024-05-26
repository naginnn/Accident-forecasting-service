//@ts-nocheck
import {FC, useState, useEffect} from "react";

import {TableBody} from "@mui/material";

import {useGetConsumersQuery, TransformConsumers} from "../api/getConsumers";

import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {TableFilter, VisibleColumnT} from "@src/widgets/tableFilter";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {PageWrapper} from "@src/entities/pageWrapper"
import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {ConsumersRow} from "./ConsumersRow";

export const TableConsumers: FC = ({}) => {
    const {data: dataConsumers, isLoading: isLoadingConsumers, error: errorConsumers} = useGetConsumersQuery()
    const [copyConsumersData, setCopyConsumersData] = useState<TransformConsumers | undefined>()


    useEffect(() => {
        if (dataConsumers) {
            setCopyConsumersData(JSON.parse(JSON.stringify(dataConsumers)))
        }
    }, [dataConsumers])


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
                                updateStatus={setCopyConsumersData}
                            />
                        )
                    })
                }
            </TableBody>
        )
    }

    return (
        <PageWrapper>
            <LoadingWrapper
                isLoading={isLoadingConsumers}
                displayType="normal"
            >
                <ErrorWrapper
                    fullSizeError={{
                        error: errorConsumers,
                        blockContent: true
                    }}
                >
                    <PaperWrapper sx={{m: '20px'}}>
                    {
                        !!copyConsumersData?.length &&
                        <TableFilter
                            id='table_view'
                            data={copyConsumersData}
                            getTableBodyLayout={getTableBodyLayout}
                            withPagination
                        >
                            <TableFilter.Banner withSearch withManageColumn/>
                            <TableFilter.SelectCell keyName='critical_status' id='critical_status'sx={{width: '50px'}} topic=''/>
                            <TableFilter.Cell keyName='consumer_address' id='consumer_address' topic='Адрес потребителя'/>
                            <TableFilter.SelectCell keyName='consumer_name' id='consumer_name' topic='Тип потребителя'/>
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
                            <TableFilter.SortCell keyName='probability' id='probability' topic='Вероятность предсказания'/>
                            <TableFilter.Cell keyName='manage_table' id='manage_table'sx={{width: '50px'}} topic=''/>
                        </TableFilter>
                    }
                    </PaperWrapper>
                </ErrorWrapper>
            </LoadingWrapper>
        </PageWrapper>
    );
};
