import {createTheme} from "@mui/material/styles";
import {ruRU} from '@mui/material/locale';

import {Button} from './components/Button'
import {TableBody} from "./components/TableBody";

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
                height: '40px',
                textTransform: 'none',
                fontWeight: 400,
            },
        },
        components: {
            MuiButton: Button,
            MuiTableBody: TableBody,
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
                        height: '40px',
                        borderRadius: '8px'
                    }
                }
            }
        }
    },
    ruRU
);