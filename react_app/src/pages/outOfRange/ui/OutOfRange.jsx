import {useNavigate} from "react-router-dom";
import {Grid, Paper, Typography} from "@mui/material";
import {getErrorMessage} from "@src/shared/lib/getErrorMessage";
import {CenteredBox} from "@src/shared/ui/centeredBox";

// Компонент обработки по переходу несуществующего пути
export const OutOfRange = () => {
    return (
        <CenteredBox position='absolute' sx={{width: '500px', height: 'max-content', zIndex: 100}}>
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
                            Страницы не существует
                        </Typography>
                    </Grid>
                </Grid>
            </Paper>
        </CenteredBox>
    )
}