import cls from "./content.module.scss"
import {ReactElement} from "react";


import {Box} from "@mui/material";

import {TopMenu} from "./TopMenu";
import {ErrorBoundary} from "@src/shared/ui/errorBoundary";
import {classNames} from "@src/shared/lib/classNames";

interface IContentProps {
    menuIsVisible: boolean
    isMenuOpen: boolean
    children: ReactElement | ReactElement[]
}

export const Content = ({menuIsVisible, isMenuOpen, children}: IContentProps) => {
    return (
        <Box sx={{flex: 1, height: 'calc(100% - 8px)', overflowX: 'auto'}}>
            <TopMenu isMenuOpen={isMenuOpen} menuIsVisible={menuIsVisible}/>
            <ErrorBoundary key={location.pathname}>
                <div className={classNames(cls.contentWrapper)}>
                    {children}
                </div>
            </ErrorBoundary>
        </Box>
    )
}