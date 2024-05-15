import {Typography, Grid, Paper} from "@mui/material";

import {CenteredBox} from "@src/shared/ui/centeredBox";

import {getErrorMessage} from "@src/shared/lib/getErrorMessage";

export const ErrorLayout = ({error = {}, position = 'absolute'}) => {
    return (
        <CenteredBox position={position} sx={{width: '500px', height: 'max-content', zIndex: 100}}>
            <Paper
                sx={{
                    width: '100%',
                    height: '100%',
                    padding: '50px',
                    bgcolor: '#ffffff',
                }}
            >
                <Grid container sx={{height: '100%'}}>
                    <Grid item alignSelf='end' xs={12}>
                        <Typography variant='h5' textAlign='center'>
                            {getErrorMessage(error)}
                        </Typography>
                    </Grid>
                </Grid>
            </Paper>
        </CenteredBox>
    )
}
