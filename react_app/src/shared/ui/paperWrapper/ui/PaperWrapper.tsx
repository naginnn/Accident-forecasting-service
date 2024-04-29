import {Paper} from "@mui/material"
import {SxProps, Theme} from "@mui/material/styles";

interface IPaperWrapper {
    children?: React.ReactNode;
    sx?: SxProps<Theme>;
    [x: string]: any;
}

export const PaperWrapper = ({children, sx, ...props}: IPaperWrapper) => {
    return (
        <Paper
            {...props}
            sx={{
                mt: '16px',
                p: '16px',
                overflow: 'auto',
                ...sx
            }}>
            {children}
        </Paper>
    )
}

