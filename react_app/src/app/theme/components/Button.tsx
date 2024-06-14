import {green, red } from "@mui/material/colors";
import {Components, Theme} from "@mui/material/styles";

declare module '@mui/material/Button' {
    interface ButtonPropsVariantOverrides {
        'main-outlined': true;
        'main-contained': true;
    }
}

export const Button: Components<Theme>['MuiButton']= {
    variants: [
        {
            props: {variant: 'main-outlined'},
            style: ({theme}: {theme: Theme}) => {
                return {
                    backgroundColor: '#ffffff',
                    padding: '5px 15px',
                    whiteSpace: 'nowrap',
                    ...theme.typography.body1,
                    color: theme.palette.text.secondary,
                    border: `1px solid rgba(210,210,210,255)`,
                    '.MuiButton-endIcon, .MuiButton-startIcon': {
                        color: theme.palette.primary.main
                    },
                    '.MuiTouchRipple-root': {
                        color: theme.palette.grey[400]
                    },
                    '&:hover': {
                        backgroundColor: theme.palette.grey[100]
                    },
                }
            },
        },
        {
            props: {variant: 'main-outlined', color: 'error'},
            style: ({theme}: {theme: Theme}) => {
                return {
                    backgroundColor: red[50],
                    padding: '5px 15px',
                    whiteSpace: 'nowrap',
                    ...theme.typography.body1,
                    color: theme.palette.error.light,
                    border: `1px solid ${theme.palette.error.light}`,
                    '.MuiButton-endIcon, .MuiButton-startIcon': {
                        color: theme.palette.error.main
                    },
                    '.MuiTouchRipple-root': {
                        color: red[400]
                    },
                    '&:hover': {
                        backgroundColor: red[100]
                    },
                }
            },
        },
        {
            props: {variant: 'main-outlined', color: 'success'},
            style: ({theme}: {theme: Theme}) => {
                return {
                    backgroundColor: green[50],
                    padding: '5px 15px',
                    whiteSpace: 'nowrap',
                    ...theme.typography.body1,
                    color: green[700],
                    border: `1px solid ${green[700]}`,
                    '.MuiButton-endIcon, .MuiButton-startIcon': {
                        color: green[700]
                    },
                    '.MuiTouchRipple-root': {
                        color: green[200]
                    },
                    '&:hover': {
                        backgroundColor: green[100]
                    },
                }
            },
        },
        {
            props: {variant: 'main-outlined', disabled: true},
            style: ({theme}: {theme: Theme}) => {
                return {
                    // backgroundColor: '#ffffff',
                    padding: '5px 15px',
                    whiteSpace: 'nowrap',
                    ...theme.typography.body1,
                    color: theme.palette.text.secondary,
                    border: `1px solid rgba(210,210,210,255)`,
                    '.MuiButton-endIcon, .MuiButton-startIcon': {
                        color: 'rgba(210,210,210,255)'
                    }
                }
            },
        },
    ],
    styleOverrides: {
        root: ({theme}) => {
            return {
                ...theme.typography.body1,
                minHeight: '40px',
                height: '40px',
                borderRadius: '8px'
            }
        },
    }
}