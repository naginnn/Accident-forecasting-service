import {FC, ReactNode} from "react";

import {Box} from "@mui/material"

interface IPagerWrapperProps {
    children: ReactNode
}

export const PageWrapper: FC<IPagerWrapperProps> = ({children}) => {
    return <Box sx={{width: '100%', height: '100%', overflow: 'auto'}}>
        {children}
    </Box>
}