import {TextField, Theme, Tooltip, TooltipProps, SxProps, Box, BoxProps, InputAdornment} from "@mui/material";

import SearchIcon from '@mui/icons-material/Search';
interface ISearchInputProps {
    value: string
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void
    tooltipTitle?: string
    tooltipPlacement?: TooltipProps["placement"]
    sx?: SxProps<Theme>
    props?: any

    [x: string]: any
}

export const SearchInput = (
    {
        tooltipTitle = '',
        tooltipPlacement = 'top',
        onChange,
        value,
        sx,
        ...props
    }: ISearchInputProps) => {

    return (
        <Tooltip title={tooltipTitle} placement={tooltipPlacement}>
            <TextField
                id="outlined-basic"
                size='small'
                label="Поиск"
                value={value}
                onChange={onChange}
                sx={{minWidth: '300px', ...sx}}
                InputProps={{
                    endAdornment: <InputAdornment position="end"><SearchIcon color='primary'/></InputAdornment>,
                }}
                {...props}/>
        </Tooltip>
    )
}