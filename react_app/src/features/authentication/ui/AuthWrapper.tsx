import cls from './authWrapper.module.css'

import Box from "@mui/material/Box";

import {classNames} from "@src/shared/lib/classNames";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";

interface IAuthWrapper {
    children: React.ReactNode;
}

export const AuthWrapper = ({children}: IAuthWrapper) => {
    return (
        <div className={classNames(cls.auth_wrapper)}>
            <Box sx={{height: '100%', pt: '20%'}}>
                <PaperWrapper sx={{width: '450px'}}>
                    {children}
                </PaperWrapper>
            </Box>
        </div>
    )
}