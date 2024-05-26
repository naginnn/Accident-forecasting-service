import {FC, useState} from "react";

import {Box, Typography} from "@mui/material";

import {BookmarksTab, BookmarksTabPanel, BookmarksTabs, BookmarksTabsList} from "@src/shared/ui/bookmarkTabs";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {Consumer} from "../types/consumerCorrelationsInfo";
import {ConsumerTable} from "./ConsumerTable";

enum TabNames {
    CONSUMERS = 'consumers',
    WARNING_CONSUMERS = 'warning_consumers'
}

interface ConsumerTablesWrapperProps {
    consumersWarn: Consumer[] | null
    consumers: Consumer[] | null
}

export const ConsumerTablesWrapper: FC<ConsumerTablesWrapperProps> = ({consumersWarn, consumers}) => {
    const [activeTab, setActiveTab] = useState<TabNames>(() => {
        return consumers ? TabNames.CONSUMERS : TabNames.WARNING_CONSUMERS
    })

    const onChangeActiveTab = (_: any, val: string | null | number) => {
        setActiveTab(val as TabNames)
    }

    return (
        <BookmarksTabs
            sx={{mt: '16px'}}
            value={activeTab}
            defaultValue={activeTab}
            onChange={onChangeActiveTab}
        >
            <BookmarksTabsList sx={{justifyContent: 'end'}}>
                <BookmarksTab
                    value={TabNames.CONSUMERS}
                >
                    Взаимосвязанные потребители
                </BookmarksTab>
                <BookmarksTab
                    value={TabNames.WARNING_CONSUMERS}
                >
                    Потребители с возможными инцидентами
                </BookmarksTab>
            </BookmarksTabsList>
            <BookmarksTabPanel value={TabNames.CONSUMERS}>
                {
                    !consumers?.length
                        ? <EmptyDataMsg/>
                        : <PaperWrapper sx={{borderTopRightRadius: 0, mt: 0}}>
                            <ConsumerTable data={consumers}/>
                        </PaperWrapper>
                }
            </BookmarksTabPanel>
            <BookmarksTabPanel value={TabNames.WARNING_CONSUMERS}>
                {
                    !consumersWarn?.length
                        ? <EmptyDataMsg/>
                        : <PaperWrapper sx={{borderTopRightRadius: 0, mt: 0}}>
                            'not check'
                        </PaperWrapper>
                }
            </BookmarksTabPanel>
        </BookmarksTabs>
    );
};

const EmptyDataMsg = () => {
    return <PaperWrapper sx={{borderTopRightRadius: 0, mt: 0}}>
        <Typography>Данные отсутствуют</Typography>
    </PaperWrapper>
}
