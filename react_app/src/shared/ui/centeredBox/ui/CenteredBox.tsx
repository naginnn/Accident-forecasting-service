import React from "react"

import Box from "@mui/material/Box";

interface ICenteredBox {
    position?: string;
    children?: React.ReactNode;
    sx?: {[x: string]: string};
    [x: string]: any
}

export const CenteredBox = ({sx, position = 'relative', children, ...props}: ICenteredBox) => {
    return (
        <Box
            sx={{
                ...sx,
                position: position,
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
            }}
            {...props}
        >
            {children}
        </Box>
    )
}