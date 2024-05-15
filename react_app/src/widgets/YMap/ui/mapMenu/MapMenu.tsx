import {FC} from "react";

import cls from './mapMenu.module.scss';

import {classNames} from "@src/shared/lib/classNames";

import {MapFilter} from "./MapFilter";

interface MapMenuProps {
    className?: string
}

export const MapMenu: FC<MapMenuProps> = ({className}) => {
    return (
        <div className={classNames(cls.map_menu, {}, [className])}>
            <MapFilter/>
        </div>
    );
};
