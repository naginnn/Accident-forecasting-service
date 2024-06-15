import * as yup from "yup";
import {FC, useEffect} from "react";
import {SubmitHandler, useForm} from "react-hook-form";
import {enqueueSnackbar} from "notistack";
import {yupResolver} from "@hookform/resolvers/yup";

import {Modal, Box, Grid, Button} from '@mui/material';
import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {ErrorWrapper} from "@src/entities/errorWrapper";
import {TextInput} from "@src/shared/ui/reactHookFormInputs";
import {CenteredBox} from "@src/shared/ui/centeredBox";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";

import {useAddEventSettingMutation} from "../api/eventSettings";


interface IFormData {
    event_name: string
}

const validationSchema = yup.object({
    event_name: yup.string().required('Обязательное поле'),
});

interface IAddDManagerModalProps {
    isOpen: boolean
    onClose: () => void
    newId: number
}

export const AddEventModal: FC<IAddDManagerModalProps> = ({isOpen, onClose, newId}) => {
    const [addEvent, {error: addError, isSuccess, isLoading}] = useAddEventSettingMutation()

    const {control, handleSubmit} = useForm({
        resolver: yupResolver(validationSchema),
        defaultValues: {event_name: ''}
    })

    useEffect(() => {
        if (isSuccess) {
            enqueueSnackbar('Событие было успешно добавлено (если не отобразилось, перезагрузите страницу)', {variant: 'success', preventDuplicate: true, key: Math.random()})
        }
    }, [isSuccess])

    const onSubmit: SubmitHandler<IFormData> = (data) => {
        addEvent({
            ...data,
            id: newId
        })
    }

    return (
        <LoadingWrapper isLoading={isLoading} displayType='modalUnblock'>
            <ErrorWrapper
                snackBarErrors={{
                    errors: [{
                        error: addError,
                        message: `Не удалось добавить новый вид события`
                    }]
                }}
            >
                <Modal open={isOpen} onClose={onClose}>
                    <Box>
                        <CenteredBox
                            position='absolute'
                            sx={{width: '500px', height: 'content'}}>
                            <PaperWrapper sx={{mt: 0}}>
                                <form onSubmit={handleSubmit(onSubmit)}>
                                    <Grid container direction='column' alignItems='center' rowSpacing={2}>
                                        <Grid item sx={{width: '100%'}}>
                                            <TextInput
                                                control={control}
                                                label='Название события'
                                                name='event_name'/>
                                        </Grid>
                                        <Grid item sx={{width: '100%'}}>
                                            <Button
                                                fullWidth
                                                type='submit'
                                                variant='main-outlined'
                                                color='success'
                                            >
                                                Добавить
                                            </Button>
                                        </Grid>
                                    </Grid>
                                </form>
                            </PaperWrapper>
                        </CenteredBox>
                    </Box>
                </Modal>
            </ErrorWrapper>
        </LoadingWrapper>
    )
}