import cls from './authWrapper.module.css'

import Box from "@mui/material/Box";

import {classNames} from "@src/shared/lib/classNames";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";
import {CenteredBox} from "@src/shared/ui/centeredBox";

interface IAuthWrapper {
    children: React.ReactNode;
}

export const AuthWrapper = ({children}: IAuthWrapper) => {
    return (
        <div className={classNames(cls.auth_wrapper)}>
            <CenteredBox position='absolute'>
                <PaperWrapper sx={{width: '450px'}}>
                    {children}
                </PaperWrapper>
            </CenteredBox>
        </div>
    )
}