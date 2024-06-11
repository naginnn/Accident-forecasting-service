import {LngLat} from "ymaps3";
import {FC, useState} from "react";

import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';

import {Box, IconButton, Slide, Tab, Tabs} from "@mui/material";

import {PaperWrapper} from "@src/shared/ui/paperWrapper";
import {YMap} from "@src/widgets/YMap";
import {coordinates} from "@src/widgets/YMap/const/coordinates";

import {ConsumerCorrelationsInfo} from "../types/consumerCorrelationsInfo";
import {ConsumersTable} from "./ConsumersTable";
import {SingleConsumerInfo} from "./SingleConsumerInfo";

interface ConsumersMainContentProps {
    data: ConsumerCorrelationsInfo
}

export const ConsumersMainContent: FC<ConsumersMainContentProps> = ({data}) => {
    const [activeTab, setActiveTab] = useState<number>(0)
    const [activeConsumer, setActiveConsumer] = useState<number | undefined>()

    return (
        <PaperWrapper sx={{mt: '16px', position: 'relative'}}>
            {
                activeConsumer !== undefined &&
                <IconButton
                    sx={{position: 'absolute', zIndex: 10, mt: '8px'}}
                    onClick={() => setActiveConsumer(undefined)}
                >
                    <ArrowBackIosIcon/>
                </IconButton>
            }
            <Box sx={{display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative'}}>
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
                        disabled={!!activeConsumer}
                    />
                    <Tab
                        label="Карта"
                        disabled={!!activeConsumer}
                    />
                </Tabs>
            </Box>
            <Slide direction="left" in={activeConsumer === undefined} mountOnEnter unmountOnExit>
                <Box>
                    {
                        data?.consumers_dep && activeTab === 0 &&
                        <ConsumersTable data={data.consumers_dep} setActiveConsumer={setActiveConsumer}/>
                    }
                    {
                        activeTab === 1 &&
                        <Box sx={{height: '600px', width: '100%', position: 'relative'}}>
                            {/*<YMap*/}
                            {/*    initLocation={{*/}
                            {/*        center: data.area?.coordinates*/}
                            {/*            .split(' ')*/}
                            {/*            .reverse() as unknown as LngLat || coordinates.moscow,*/}
                            {/*        zoom: 13*/}
                            {/*    }}*/}
                            {/*/>*/}
                        </Box>
                    }
                </Box>
            </Slide>
            <Slide direction="left" in={activeConsumer !== undefined} mountOnEnter unmountOnExit>
                {
                    activeConsumer
                        ? <Box>
                            <SingleConsumerInfo
                                consumerId={activeConsumer}
                            />
                        </Box>
                        : <div/>
                }
            </Slide>
        </PaperWrapper>
    );
};
