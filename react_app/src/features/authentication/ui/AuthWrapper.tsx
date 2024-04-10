import React from "react";
import { CenteredBox } from "../../../shared/ui/centeredBox";


interface IAuthWrapper {
    children: React.ReactNode;
    sx?: {[x: string]: string};
}

export const AuthWrapper = ({children, sx = {}}: IAuthWrapper) => {
    return (
        <CenteredBox position='absolute' sx={{padding: '16px', width: '400px', bgcolor: 'white', ...sx}}>
            {children}
        </CenteredBox>
    )
}