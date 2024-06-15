import {FC} from "react";
import {green, red} from "@mui/material/colors";

import AddIcon from '@mui/icons-material/Add';
import ClearIcon from '@mui/icons-material/Clear';

import {Box, Divider, IconButton, Typography} from "@mui/material";

import {ErrorWrapper} from "@src/entities/errorWrapper";
import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {useToggle} from "@src/shared/hooks/useToggle";

import {useDeleteEventSettingMutation, useGetEventsSettingQuery} from "../api/eventSettings";
import {AddEventModal} from "./addEventModal";

export const Events: FC = () => {
    const {on: openAddEventMdl, off: closeAddEventMdl, value: isOpenAddEventMdl} = useToggle()

    const {data: events, error: errorEvents, isLoading: isLoadingEvents} = useGetEventsSettingQuery()
    const [deleteEvent, {isLoading, error: errorDeleteEvent}] = useDeleteEventSettingMutation()


    return (
        <ErrorWrapper
            snackBarErrors={{
                errors: [
                    {error: errorEvents, message: 'Не удалось загрузить виды событий', blockContent: true},
                    {error: errorDeleteEvent, message: 'Не удалось удалить событие'},
                ],

            }}
        >
            {
                isOpenAddEventMdl &&
                <AddEventModal
                    isOpen={isOpenAddEventMdl}
                    onClose={closeAddEventMdl}
                    newId={events?.length ? events?.length + 1 : Math.floor(Math.random() * 1000)}
                />
            }
            <Box sx={{pr: '16px'}}>
                <Box sx={{display: 'flex', mb: '8px', justifyContent: 'space-between'}}>
                    <Typography variant='h5' gutterBottom>
                        Виды событий
                    </Typography>
                    <IconButton sx={{color: green[500]}} onClick={openAddEventMdl}>
                        <AddIcon/>
                    </IconButton>
                </Box>
                <Divider/>
                <LoadingWrapper isLoading={isLoadingEvents} displayType='linear'>
                    {
                        events?.length
                            ? events.map((info) => {
                                return (
                                    <React.Fragment key={info.id}>
                                        <Box sx={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'center',
                                            my: '2px'
                                        }}>
                                            <Typography variant='body2'>
                                                {info.event_name}
                                            </Typography>
                                            <IconButton sx={{color: red[800]}}>
                                                <ClearIcon
                                                    onClick={() => deleteEvent(info.id)}
                                                    fontSize='small'
                                                />
                                            </IconButton>
                                        </Box>
                                        <Divider/>
                                    </React.Fragment>
                                )
                            })
                            : <Typography>Данные отсутствуют</Typography>
                    }
                </LoadingWrapper>
            </Box>
        </ErrorWrapper>
    );
};
