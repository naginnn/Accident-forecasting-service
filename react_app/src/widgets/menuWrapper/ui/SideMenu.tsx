import cls from './sideMenu.module.scss'
import {useNavigate} from "react-router-dom";

import {routerPaths} from "@src/shared/config/router";
import {AppRoutes} from "@src/shared/config/router/ui/router"
import {classNames} from '@src/shared/lib/classNames';

import {Divider} from "@mui/material"

import LogoutIcon from '@mui/icons-material/Logout';

import {ToggleIcon} from "./ToggleIcon";
import {Row} from "./row/Row";
import {internalLinks} from '../const/internalLinks';

interface IMenuProps {
    isOpen: boolean
    onToggle: () => void
}

export const SideMenu = ({isOpen, onToggle}: IMenuProps) => {
    const navigate = useNavigate()

    const logout = () => {
        localStorage.removeItem('token')
        navigate(routerPaths[AppRoutes.LOGIN])
    }

    return (
        <div className={classNames(cls.sideMenu, {[cls['sideMenu-open']]: isOpen})}>
            <ToggleIcon isOpen={isOpen} onToggle={onToggle}/>
            <div className={classNames(cls.optionList)}>
                {
                    internalLinks.map(link => {
                        return <Row
                            key={link.topic}
                            isOpenMenu={isOpen}
                            topic={link.topic}
                            icon={link.icon}
                            url={link.url}
                            extensiableLinks={link.extensiableLinks}
                            id={link.id}
                        />
                    })
                }
            </div>
            <div className={classNames(cls.exitIcon)}>
                <Divider sx={{mb: '8px'}}/>
                <Row
                    isOpenMenu={isOpen}
                    topic='Выйти'
                    icon={<LogoutIcon/>}
                    onRowClick={logout}
                />
            </div>
        </div>
    )
}