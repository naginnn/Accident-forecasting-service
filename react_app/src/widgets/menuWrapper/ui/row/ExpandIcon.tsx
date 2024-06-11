import cls from './expandIcon.module.scss'
import {FC, Dispatch, SetStateAction, MouseEventHandler} from "react";

import {classNames} from '@src/shared/lib/classNames';


import {useTheme} from "@mui/material";

import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

interface IExpandIconProps {
    isOpenExtLinks: boolean
    setIsOpenExtLinks: Dispatch<SetStateAction<boolean>>
}

export const ExpandIcon: FC<IExpandIconProps> = ({setIsOpenExtLinks, isOpenExtLinks}) => {
    const {palette} = useTheme()

    const onClickExtIcon: MouseEventHandler<HTMLDivElement> = (e) => {
        if (e.button === 0) {
            e.stopPropagation()

            setIsOpenExtLinks(prev => !prev)
        }
    }

    return <div onMouseDown={onClickExtIcon} className={classNames(cls.expandIconWrapper)}>
        {
            isOpenExtLinks
                ? <ExpandLessIcon sx={{color: palette.primary.main}}/>
                : <ExpandMoreIcon sx={{color: palette.primary.main}}/>
        }
    </div>
}