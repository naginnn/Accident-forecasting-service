import {createTheme} from "@mui/material/styles";
import {ruRU} from '@mui/material/locale';

export const theme = createTheme(
    {
        typography: {
            button: {
                textTransform: 'none',
                fontWeight: 400,
            },
        },
        components: {
            MuiPaper: {
                styleOverrides: {
                    root: {
                        borderRadius: '8px'
                    }
                }
            },
            MuiInputBase: {
                defaultProps: {
                    sx: {
                        borderRadius: '8px'
                    }
                }
            }
        }
    },
    ruRU
);