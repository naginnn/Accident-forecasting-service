import {FC} from "react";

import {Divider, Grid, Table, TableBody, TableRow, TableCell, Typography} from "@mui/material";

import {renameObject} from "@src/shared/lib/renameObject";

import {Consumer} from "../types/consumerCorrelationsInfo";
import {consumersName} from "../const/consumersName";

interface SingleConsumerInfoProps {
    consumer: Consumer
}

export const SingleConsumerInfo: FC<SingleConsumerInfoProps> = ({consumer}) => {

    return <Grid container alignItems='start' columnSpacing={2} sx={{mt: '16px'}}>

        <Grid item xs sx={{paddingRight: '16px'}}>
            <Typography variant='h5' gutterBottom>
                Основная информация о потребителе
            </Typography>
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
        <Divider orientation="vertical" variant="middle" flexItem />
        <Grid item xs sx={{height: '500px'}}>
            <Typography variant='h5' gutterBottom>
                Температурный график
            </Typography>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Asperiores aut dolore harum illum, impedit itaque nihil nisi porro quia repudiandae totam unde vero vitae. Excepturi fugit mollitia necessitatibus tempora ullam?
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Asperiores aut dolore harum illum, impedit itaque nihil nisi porro quia repudiandae totam unde vero vitae. Excepturi fugit mollitia necessitatibus tempora ullam?
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Asperiores aut dolore harum illum, impedit itaque nihil nisi porro quia repudiandae totam unde vero vitae. Excepturi fugit mollitia necessitatibus tempora ullam?
        </Grid>
    </Grid>
};
