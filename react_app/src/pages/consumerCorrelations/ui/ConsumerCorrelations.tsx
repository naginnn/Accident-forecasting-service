import {FC} from "react";
import {useNavigate, useParams} from "react-router-dom";

import {Box, Breadcrumbs, Grid} from "@mui/material";


import {PageWrapper} from "@src/entities/pageWrapper";
import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {withMenu} from "@src/widgets/menuWrapper";
import {Link} from "@src/shared/ui/link";
import {routerPaths} from "@src/shared/config/router";
import {AppRoutes} from "@src/shared/config/router/ui/router";

import {useGetConsumersCorrelationsQuery} from "../api/getConsumerCorrelations";
import {ConsumersMainContent} from "./ConsumersMainContent";
import {CommonInfoBlock} from "./CommonInfoBlock";

export const ConsumerCorrelations: FC = withMenu(() => {
    const navigate = useNavigate()
    const {consumer_stations_id} = useParams()

    const {data, error, isLoading} = useGetConsumersCorrelationsQuery(consumer_stations_id!)

    return (
        <Box sx={{overflow: 'hidden'}}>
            <Breadcrumbs>
                <Link
                    sx={{color: 'black'}}
                    onClick={() => navigate(routerPaths[AppRoutes.CONSUMERS])}
                >
                    Потребители
                </Link>
                {
                    data?.consumer_stations?.address &&
                    <Link sx={{color: 'black'}}>
                        ЦТП &nbsp;
                        {data.consumer_stations.address}
                    </Link>
                }
            </Breadcrumbs>
            <PageWrapper sx={{mt: '16px'}}>
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
        </Box>
    );
}, 'Потребители')

