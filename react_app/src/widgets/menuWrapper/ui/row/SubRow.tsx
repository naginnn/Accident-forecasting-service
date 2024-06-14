import cls from './subRow.module.scss'
import {MouseEventHandler} from "react";
import {useNavigate} from "react-router-dom";

import {Typography} from "@mui/material";

import {openNewWindowPage} from '@src/shared/lib/openNewWindowPage';
import {useAppDispatch} from '@src/shared/model/store';
import {classNames} from '@src/shared/lib/classNames';


interface ISubRowProps {
    url: string
    topic: string
    activeIdTab: string
    id: string
}

export const SubRow = ({topic, url, activeIdTab, id}: ISubRowProps) => {
    const dispatch = useAppDispatch()
    const navigate = useNavigate()

    const onNavigate: MouseEventHandler<HTMLDivElement> = (e) => {
        e.stopPropagation()
        if (e.button === 0) {
            navigate(url)
        } else if (e.button === 1) {
            openNewWindowPage(url)
        }
    }

    return (
        <div
            className={classNames(cls.subRowWrapper, {[cls['subRowWrapper-active']]: activeIdTab === id})}
            onMouseDown={onNavigate}
        >
            <Typography variant='body2'>
                {topic}
            </Typography>
        </div>
    )
}