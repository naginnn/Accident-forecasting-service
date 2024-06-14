import {FC, ReactNode} from "react";

import {Box, SxProps, Theme} from "@mui/material"

interface IPagerWrapperProps {
    children: ReactNode

    sx?: SxProps<Theme>
}

export const PageWrapper: FC<IPagerWrapperProps> = ({children, sx = {}}) => {
    return <Box sx={{width: '100%', height: '100%', overflow: 'auto', ...sx}}>
        {children}
    </Box>
}