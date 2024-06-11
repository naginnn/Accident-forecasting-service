import {FC} from "react";
import {useParams} from "react-router-dom";

import {Grid} from "@mui/material";


import {PageWrapper} from "@src/entities/pageWrapper";
import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {withMenu} from "@src/widgets/menuWrapper";

import {useGetConsumersCorrelationsQuery} from "../api/getConsumerCorrelations";
import {ConsumersMainContent} from "./ConsumersMainContent";
import {CommonInfoBlock} from "./CommonInfoBlock";

export const ConsumerCorrelations: FC = withMenu(() => {
    const {consumer_stations_id} = useParams()

    const {data, error, isLoading} = useGetConsumersCorrelationsQuery(consumer_stations_id!)

    return (
        <PageWrapper>
            <LoadingWrapper
                isLoading={isLoading}
                displayType='normal'
            >
                <ErrorWrapper
                    fullSizeError={{
                        error,
                        blockContent: true
                    }}
                >
                    {
                        data &&
                        <>
                            <Grid container columnSpacing={2}>
                                <Grid item sx={{flex: '0 0 500px'}}>
                                    <CommonInfoBlock
                                        weather={data.weather}
                                        areaName={data.area?.name}
                                        srcStations={data.source_stations}
                                        consumerStationName={data.consumer_stations?.name}
                                        consumerStationAddr={data.consumer_stations?.address}
                                    />
                                </Grid>
                            </Grid>
                            <ConsumersMainContent data={data}/>
                        </>
                    }
                </ErrorWrapper>
            </LoadingWrapper>
        </PageWrapper>
    );
}, 'Потребители')

