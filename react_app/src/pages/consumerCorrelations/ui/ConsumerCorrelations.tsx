import {FC} from "react";
import {useParams} from "react-router-dom";
import {LngLat} from "@yandex/ymaps3-types";

import {Box, Grid} from "@mui/material";

import {PageWrapper} from "@src/entities/pageWrapper";
import {YMap} from "@src/widgets/YMap";
import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";
import {coordinates} from "@src/widgets/YMap/const/coordinates";

import {useGetConsumersCorrelationsQuery} from "../api/getConsumerCorrelations";
import {CommonInfoBlock} from "./CommonInfoBlock";

export const ConsumerCorrelations: FC = () => {
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
                                <Grid item xs>
                                    <PaperWrapper>
                                        main
                                    </PaperWrapper>
                                </Grid>
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
                            <Box sx={{height: '600px', width: '100%', position: 'relative', mt: '16px'}}>
                                <YMap initLocation={{
                                    center: data.area?.coordinates
                                        .split(' ')
                                        .reverse() as unknown as LngLat || coordinates.moscow,
                                    zoom: 13
                                }}/>
                            </Box>
                        </>
                    }
                </ErrorWrapper>
            </LoadingWrapper>
        </PageWrapper>
    );
};

