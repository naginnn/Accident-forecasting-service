import {createTheme} from "@mui/material/styles";
import {ruRU} from '@mui/material/locale';

export const theme = createTheme(
    {
        typography: {
            fontFamily: [
                "Montserrat",
                '-apple-system',
                'BlinkMacSystemFont',
                'Segoe UI',
                'Roboto',
                'Oxygen',
                'Ubuntu',
                'Cantarell',
                'Fira Sans',
                'Droid Sans',
                'Helvetica Neue',
            ].join(','),
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