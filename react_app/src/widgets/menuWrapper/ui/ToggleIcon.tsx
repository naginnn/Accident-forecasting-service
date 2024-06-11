import cls from './toggleIcon.module.scss'
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';

import {Divider} from "@mui/material";

import {classNames} from '@src/shared/lib/classNames';
import {FocusedIcon} from '@src/shared/ui/focusedIcon';

interface ILogoProps {
    isOpen: boolean
    onToggle: () => void
}

export const ToggleIcon = ({isOpen, onToggle}: ILogoProps) => {
    return (
        <div className={classNames(cls.toggleIconWrapper)}>
            <div className={classNames(cls.toggleIcon)}>
                <FocusedIcon onClick={onToggle} sx={{ml: 'auto', height: '40px'}}>
                    {
                        isOpen
                            ? <CloseIcon/>
                            : <MenuIcon/>
                    }
                </FocusedIcon>
            </div>
            <Divider/>
        </div>
    )
}