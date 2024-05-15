import {forwardRef} from "react";
import {BaseVariant, CustomContentProps, SnackbarContent, useSnackbar} from "notistack";
import {green, red} from "@mui/material/colors";

import CloseIcon from '@mui/icons-material/Close';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

import {styled} from "@mui/system";
import {IconButton, PaperProps, Paper, Theme, Typography} from "@mui/material";

import {SxProps} from "@mui/material/styles";

export const NotistackAlertContent = styled(Paper)<PaperProps & { ownerState: { variant: NotistackAlertT["variant"] } }>(({ownerState}) => {
    let rootStyle: SxProps<Theme> = {
        maxWidth: '400px',
        width: '400px',
        minHeight: '30px',
        padding: '10px 20px',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
    }

    if (ownerState.variant === 'error') {
        rootStyle = {
            ...rootStyle,
            backgroundColor: red[50],
            '.MuiSvgIcon-root': {
                color: red[400]
            },
            '.MuiButtonBase-root': {
                '.MuiSvgIcon-root': {
                    color: 'black'
                }
            }
        }
    } else if (ownerState.variant === 'success') {
        rootStyle = {
            ...rootStyle,
            backgroundColor: green[50],
            '.MuiSvgIcon-root': {
                color: green[700]
            },
            '.MuiButtonBase-root': {
                '.MuiSvgIcon-root': {
                    color: 'black'
                }
            }
        }
    }

    return ({'&.MuiPaper-root': rootStyle,})
})

type NotistackAlertT = CustomContentProps & { variant: BaseVariant }

export const NotistackAlert = forwardRef<HTMLDivElement, NotistackAlertT>(({id, ...props}: NotistackAlertT, ref) => {
    const {closeSnackbar} = useSnackbar()

    const getIcon = () => {
        switch (props.variant) {
            case 'success':
                return <CheckCircleOutlineIcon fontSize='small' sx={{mr: '8px'}}/>
            case 'error':
                return <ErrorOutlineIcon fontSize='small' sx={{mr: '8px'}}/>
            default:
                return null
        }
    }

    return (
        <SnackbarContent ref={ref}>
            <NotistackAlertContent ownerState={{
                variant: props.variant
            }}>
                {getIcon()}
                <Typography variant='body2' sx={{mr: '8px'}}>
                    {props.message}
                </Typography>
                <IconButton
                    size="small"
                    aria-label="close"
                    color="inherit"
                    sx={{ml: 'auto'}}
                    onClick={() => closeSnackbar(id)}
                >
                    <CloseIcon fontSize='small'/>
                </IconButton>
            </NotistackAlertContent>
        </SnackbarContent>
    )

})