import {FC, useMemo, useState} from "react";

import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';

import {Box, IconButton, Slide, Tab, Tabs} from "@mui/material";

import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {ConsumersTable} from "./consumersTable/ConsumersTable";
import {SingleConsumerInfo} from "./singleConsumer/SingleConsumerInfo";
import {ConsumersMap} from "./consumersMap/ConsumersMap";
import {CriticalStatusName, FormattedConsumer} from "../types/formattedConsumer";
import {FormattedConsumerCorrelationsInfo} from "../api/getConsumerCorrelations";

interface ConsumersMainContentProps {
    data: FormattedConsumerCorrelationsInfo
}

export const ConsumersMainContent: FC<ConsumersMainContentProps> = ({data}) => {
    const [activeTab, setActiveTab] = useState<number>(0)
    const [activeConsumer, setActiveConsumer] = useState<FormattedConsumer | undefined>()

    const isIncident = useMemo(() => {
        return !!data.consumers_dep?.some(info => {
            return info.critical_status !== CriticalStatusName.IS_NO_ACCENDENT
        })
    }, [data])

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
                        <ConsumersTable
                            consumerStationId={data.consumer_stations?.id}
                            data={data.consumers_dep}
                            setActiveConsumer={setActiveConsumer}
                        />
                    }
                    {
                        activeTab === 1 && data &&
                        <ConsumersMap info={data} setActiveConsumer={setActiveConsumer}/>
                    }
                </Box>
            </Slide>
            <Slide direction="left" in={activeConsumer !== undefined} mountOnEnter unmountOnExit>
                {
                    activeConsumer
                        ? <Box>
                            <SingleConsumerInfo
                                isIncident={isIncident}
                                consumer={activeConsumer}
                            />
                        </Box>
                        : <div/>
                }
            </Slide>
        </PaperWrapper>
    );
};
