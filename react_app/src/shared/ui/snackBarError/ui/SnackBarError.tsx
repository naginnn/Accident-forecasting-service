import {useState, SyntheticEvent} from "react";
import {SxProps, Theme} from '@mui/material/styles';

import {Portal} from '@mui/base/Portal';
import {Alert, Box, Snackbar} from "@mui/material";

interface ISnackBarError {
    closeHandler?: Function
    autoHideDuration?: number
    children: string
    sx?: SxProps<Theme>

    [x: string]: any
}

/*
    Устаревшее отображение
    TODO везде где используется переделать на notistackAlert

    closeHandler - callback вызвающийся при закрытии ошибки
    autoHideDuration - время после которого ошибка закрывается автоматически
    sx - стили
    children - текс ошибки
*/
export const SnackBarError = ({closeHandler, autoHideDuration = 6000, sx, children, ...props}: ISnackBarError) => {
    const [isError, setIsError] = useState(true);

    const onClose = (event?: SyntheticEvent | Event, reason?: string) => {
        if (reason === 'clickaway')
            return

        if (closeHandler) {
            closeHandler()
        }

        setIsError(false)
    }

    return (
        <Portal>
            <Snackbar
                onClick={(e) => e.stopPropagation()}
                {...props}
                onClose={onClose}
                open={isError}
                autoHideDuration={autoHideDuration}
                sx={{...sx}}>
                <Box>
                    <Alert
                        severity="error"
                        sx={{border: '1px solid #ffcdcc'}}>
                        {children}
                    </Alert>
                </Box>
            </Snackbar>
        </Portal>
    )
};