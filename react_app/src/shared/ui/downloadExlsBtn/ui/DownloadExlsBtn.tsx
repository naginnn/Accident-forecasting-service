import {SxProps, Theme} from "@mui/material/styles";

import DownloadSharpIcon from '@mui/icons-material/DownloadSharp';
import {Button} from "@mui/material";

interface IDownloadExcelButtonProps {
    sx?: SxProps<Theme>
    children: string

    [x: string]: any
}

// Кнопка загрузки excel
// children - текст кнопки
export const DownloadExcelButton = ({sx, children, ...props}: IDownloadExcelButtonProps) => {
    return (
        <Button
            variant='main-outlined'
            {...props}
            sx={{...sx}}
            endIcon={<DownloadSharpIcon/>}
        >
            {children}
        </Button>
    )
}