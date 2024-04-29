import {SxProps, Theme} from "@mui/material";
import Box from "@mui/material/Box";

interface ICenteredBox {
    position?: 'absolute' | 'relative';
    children?: React.ReactNode;
    sx?: SxProps<Theme>

    [x: string]: any
}

export const CenteredBox = ({sx = {}, position = 'relative', children, ...props}: ICenteredBox) => {
    return (
        <Box
            sx={{
                position: position,
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                ...sx,
            }}
            {...props}
        >
            {children}
        </Box>
    )
}