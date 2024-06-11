import cls from './row.module.scss';
import {ReactElement, useEffect, useMemo, useState, MouseEvent, MouseEventHandler} from "react";
import {useLocation, useNavigate} from "react-router-dom";

import {Box, Tooltip, Typography} from "@mui/material";

import {useAppDispatch, useAppSelector} from '@src/shared/model/store';
import {classNames} from '@src/shared/lib/classNames';
import {FocusedIcon} from '@src/shared/ui/focusedIcon';
import {openNewWindowPage} from '@src/shared/lib/openNewWindowPage';

import {ExpandIcon} from "./ExpandIcon";
import {SubRow} from "./SubRow";
import {InternalLinkT} from "../../const/internalLinks";
import {activeMenuTabIdSelector, openedTabsSelector, setActivePageId} from "../../store";

interface IRowProps {
    isOpenMenu: boolean
    topic: string
    icon: ReactElement
    id?: string
    url?: string
    onRowClick?: (e: MouseEvent<HTMLTableRowElement, MouseEvent>) => void
    extensiableLinks?: InternalLinkT['extensiableLinks']
}

export const Row = (
    {
        isOpenMenu,
        url,
        extensiableLinks,
        onRowClick,
        topic,
        icon,
        id
    }: IRowProps) => {
    const navigate = useNavigate()
    const dispatch = useAppDispatch()
    const {pathname} = useLocation()
    const openedTabs = useAppSelector(openedTabsSelector)
    const activeIdTab = useAppSelector(activeMenuTabIdSelector)

    const [isOpenExtLinks, setIsOpenExtLinks] = useState<boolean>(() => {
        if (url && url in openedTabs)
            return true
        return false
    })

    useEffect(() => {
        if (extensiableLinks?.length) {
            extensiableLinks.forEach(({url}) => {
                if (url === pathname)
                    setIsOpenExtLinks(true)
            })
        }
    }, [pathname, extensiableLinks])

    const onRowClickInternal: MouseEventHandler<HTMLDivElement> = (e: any) => {
        if (onRowClick && typeof onRowClick === 'function') {
            onRowClick(e)
        } else if (url && e.button === 1) {
            openNewWindowPage(url)
            dispatch(setActivePageId(url))
        } else if (url && e.button === 0) {
            navigate(url)
            dispatch(setActivePageId(url))
        }
    }

    const getExtLinks = () => {
        if (!isOpenMenu || !extensiableLinks?.length || !isOpenExtLinks)
            return null

        return <Box sx={{my: '4px'}}>
            {
                extensiableLinks.map(({topic, url, id}) => (
                    <SubRow
                        key={url}
                        url={url}
                        topic={topic}
                        id={id}
                        activeIdTab={activeIdTab}
                    />
                ))
            }
        </Box>
    }

    const isActiveRow = useMemo(() => {
        let isActive = false

        const existInExtLinks = () => {
            return !!extensiableLinks?.some(({id}) => id === activeIdTab)
        }

        if (id) {
            if ((!isOpenMenu || !isOpenExtLinks) && (existInExtLinks() || activeIdTab === id)) {
                isActive = true
            } else if (isOpenMenu && isOpenExtLinks && !existInExtLinks() && activeIdTab === id) {
                isActive = true
            } else if (!extensiableLinks?.length && activeIdTab === id) {
                isActive = true
            }
        }

        return isActive
    }, [extensiableLinks, isOpenExtLinks, isOpenMenu, activeIdTab])

    return (
        <div>
            <div
                className={classNames(cls.rowWrapper, {[cls['rowWrapper-active']]: isActiveRow})}
                onMouseDown={onRowClickInternal}
            >
                <div className={classNames(cls.iconWrapper)}>
                    <Tooltip
                        placement='right'
                        title={isOpenMenu ? '' : topic}
                        sx={{color: (theme) => theme.palette.primary.main}}
                    >
                        <Box>
                            <FocusedIcon disabledFocus={true}>
                                {icon}
                            </FocusedIcon>
                        </Box>
                    </Tooltip>
                </div>
                <div className={classNames(cls.textWrapper, {[cls['textWrapper-open']]: isOpenMenu})}>
                    <div className={classNames(cls.text, {[cls['text-open']]: isOpenMenu})}>
                        <Typography variant='body2'>
                            {topic}
                        </Typography>
                    </div>
                </div>
                {
                    extensiableLinks?.length && isOpenMenu &&
                    <ExpandIcon isOpenExtLinks={isOpenExtLinks} setIsOpenExtLinks={setIsOpenExtLinks}/>
                }
            </div>
            {getExtLinks()}
        </div>
    )
}
