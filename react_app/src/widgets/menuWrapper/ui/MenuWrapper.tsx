import {ReactElement, useMemo, FC} from 'react';
import {useLocation} from "react-router-dom";

import {Box, useTheme} from "@mui/material";

import {useWindowSize} from '@src/shared/hooks/useWindowSize';
import {routerPaths} from "@src/shared/config/router";
import {AppRoutes} from "@src/shared/config/router/ui/router";

import {isMenuOpenSelector, onToggleMenuState} from "../store";

import {SideMenu} from "./SideMenu";
import {Content} from "./Content";
import { useAppDispatch, useAppSelector } from '@src/shared/model/store';


interface IPageProps {
    children: ReactElement
}

export const MenuWrapper: FC<IPageProps> = ({children}: IPageProps) => {
    const location = useLocation()
    const dispatch = useAppDispatch()

    const isMenuOpen = useAppSelector(isMenuOpenSelector)

    const {width: windowWidth} = useWindowSize()

    const isShowOverlay = useMemo(() => {
        return windowWidth <= 1400 && isMenuOpen
    }, [windowWidth, isMenuOpen])

    const menuIsVisible = location.pathname !== routerPaths[AppRoutes.LOGIN]
        && location.pathname !== routerPaths[AppRoutes.REGISTRATION]

    const onToggleMenu = () => {
        dispatch(onToggleMenuState())
    }

    return (
        <Box sx={{
            width: '100%',
            height: '100%',
            display: 'flex',
            overflowX: 'hidden'
        }}>
            {
                menuIsVisible &&
                <>
                    <Overlay isShowOverlay={isShowOverlay}/>
                    <SideMenu isOpen={isMenuOpen} onToggle={onToggleMenu}/>
                </>
            }
            <Content
                menuIsVisible={menuIsVisible}
                isMenuOpen={isMenuOpen}
            >
                {children}
            </Content>
        </Box>
    );
}

interface IOverlayProps {
    isShowOverlay: boolean
}

const Overlay = ({isShowOverlay}: IOverlayProps) => {
    const {palette} = useTheme()

    return (
        <Box
            sx={{
                display: isShowOverlay ? 'initial' : 'none',
                position: 'absolute',
                overflowX: 'hidden',
                height: '100%',
                zIndex: 10000,
                background: palette.grey[900],
                opacity: '0.1',
                width: '100%',
                top: 0,
                left: 0
            }}
        />
    )
}
