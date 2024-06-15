import {FC} from "react";

import {Divider, Box, Grid, Table, TableBody, TableRow, TableCell, Typography} from "@mui/material";

import {renameObject} from "@src/shared/lib/renameObject";
import {CollapsedBlock} from "@src/entities/collapsedBlock";
import {DownloadExcelButton} from "@src/shared/ui/downloadExlsBtn";
import {ErrorWrapper} from "@src/entities/errorWrapper";

import {consumersName} from "../../const/consumersName";
import {TempDroppingChart} from "./TempDroppingChart";
import {EventsTable} from "./EventsTable";
import {useDownloadConsumer} from "../../api/downloadExcel";
import {CounterEventsTable} from "./CounterEventsTable";
import {CriticalStatusName, FormattedConsumer} from "../../types/formattedConsumer";


interface SingleConsumerInfoProps {
    consumer: FormattedConsumer
    isIncident: boolean
}

export const SingleConsumerInfo: FC<SingleConsumerInfoProps> = ({consumer, isIncident}) => {
    const {downloadExcel, error} = useDownloadConsumer()

    return <ErrorWrapper
        snackBarErrors={{
            errors: [{error, message: 'Не удалось загрузить excel'}]
        }}
    >
        <Grid container alignItems='start' columnSpacing={2} sx={{mt: '16px'}}>
            <Grid item xs sx={{paddingRight: '16px'}}>
                <Box sx={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
                    <Typography variant='h5' gutterBottom sx={{display: 'inline-block'}}>
                        Основная информация о потребителе
                    </Typography>
                    <DownloadExcelButton
                        sx={{width: '190px'}}
                        onClick={() => downloadExcel(consumer.id)}
                    >
                        Загрузить excel
                    </DownloadExcelButton>
                </Box>
                <Table size='small' sx={{pr: '16px'}}>
                    <TableBody>
                        {
                            Object.entries(renameObject(consumersName, consumer, true))
                                .map(([key, val]) => {
                                    return <TableRow key={key} sx={{'&:last-child td, &:last-child th': {border: 0}}}>
                                        <TableCell sx={{width: '35%', fontWeight: 500}}>
                                            {key}
                                        </TableCell>
                                        <TableCell sx={{width: '65%'}}>
                                            {val}
                                        </TableCell>
                                    </TableRow>
                                })
                        }
                    </TableBody>
                </Table>
            </Grid>
            {
                isIncident &&
                <>
                    <Divider orientation="vertical" variant="middle" flexItem/>
                    <Grid item xs sx={{height: '500px'}}>
                        <Typography variant='h5' gutterBottom>
                            График падения температуры
                        </Typography>
                        {
                            consumer.weather_fall[0]?.temp_dropping?.temp_data?.length
                                ? <TempDroppingChart data={consumer.weather_fall[0].temp_dropping.temp_data}/>
                                : <Typography>Данные отсутствуют</Typography>
                        }
                    </Grid>
                </>
            }
        </Grid>
        <Box sx={{mt: '16px'}}>
            <CollapsedBlock topicName='Инциденты на потребителях'>
                <EventsTable consumerId={consumer.id}/>
            </CollapsedBlock>
            <CollapsedBlock topicName='Выгрузка ОДПУ отопления'>
                <CounterEventsTable consumerId={consumer.id}/>
            </CollapsedBlock>
        </Box>
    </ErrorWrapper>
};
