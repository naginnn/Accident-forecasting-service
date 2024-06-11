import {FC, useEffect, useState} from "react";

import {Box, Tab, Tabs} from "@mui/material";

import {TransformConsumers, useGetConsumersQuery} from "@src/pages/consumers/api/getConsumers";

import {withMenu} from "@src/widgets/menuWrapper";
import {PageWrapper} from "@src/entities/pageWrapper";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";
import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {TableConsumers} from "@src/pages/consumers/ui/TableConsumers";

import {ConsumerMap} from "./map/ConsumerMap";

export const ConsumersWrapper: FC = withMenu(({}) => {
    const {data: dataConsumers, isLoading: isLoadingConsumers, error: errorConsumers} = useGetConsumersQuery()

    const [copyConsumersData, setCopyConsumersData] = useState<TransformConsumers[]>([])
    const [activeTab, setActiveTab] = useState<number>(1)

    useEffect(() => {
        if (dataConsumers) {
            setCopyConsumersData(JSON.parse(JSON.stringify(dataConsumers)))
        }
    }, [dataConsumers])

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
                    <PaperWrapper sx={{m: 0}}>
                        <Box sx={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            position: 'relative'
                        }}>
                            <Tabs
                                sx={{borderColor: 'divider', border: '1px solid #bbdefb', borderRadius: '8px'}}
                                value={activeTab}
                                onChange={(event: React.SyntheticEvent, newValue: number) => {
                                    setActiveTab(newValue)
                                }}
                            >
                                <Tab
                                    label="Таблица"
                                    sx={{borderRight: '1px solid #bbdefb'}}
                                />
                                <Tab label="Карта"/>
                            </Tabs>
                        </Box>
                        {
                            !!copyConsumersData?.length && activeTab === 0 &&
                            <TableConsumers
                                data={copyConsumersData}
                                updateStatus={setCopyConsumersData}
                            />
                        }
                        {
                            !!copyConsumersData?.length && activeTab === 1 &&
                            <ConsumerMap data={copyConsumersData}/>
                        }
                    </PaperWrapper>
                </ErrorWrapper>
            </LoadingWrapper>
        </PageWrapper>
    );
}, 'Потребители')
