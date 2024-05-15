import {FC, useContext, useState} from "react";
import {LngLat} from "ymaps3";

import cls from './mapFilter.module.scss'

import {Box, MenuItem} from "@mui/material";
import Select, { SelectChangeEvent } from "@mui/material/Select";


import {CollapsedBlock} from "@src/entities/collapsedBlock";
import {classNames} from "@src/shared/lib/classNames";
import { SearchInput } from "@src/shared/ui/searchInput";

import {coordinates} from "../../const/coordinates";
import {MapContext} from "../../model/context";

interface MapFilterProps {
    className?: string
}

export const MapFilter: FC<MapFilterProps> = ({className}) => {
    const [searchedVal, setSearchedVal] = useState<string>('')
    const [activeCounty, setActiveCounty] = useState<string>('')

    const {setLocation} = useContext(MapContext)

    const onSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchedVal(e.target.value)
    }

    const onChangeCounty = (e: SelectChangeEvent<string>) => {
        if (e.target.value) {
            const lngLat = e.target.value.split(';') as unknown as LngLat

            setLocation({
                center: lngLat,
                zoom: 13,
                duration: 3000
            })
            setActiveCounty(e.target.value)
        }
    }

    return (
        <div className={classNames(cls.filter_wrapper, {}, [className])}>
            <SearchInput
                value={searchedVal}
                onChange={onSearch}
                sx={{width: '100%'}}
            />
            <Box sx={{mt: '16px'}}>
                <CollapsedBlock
                    textPlacement='right'
                    topicName='Доп. фильтры'
                >
                    <Select
                        labelId='county'
                        label='Округ'
                        id='county'
                        onChange={onChangeCounty}
                        value={activeCounty}
                        sx={{mt: '8px'}}
                        fullWidth
                    >
                        {
                            coordinates.countyCoordinates.map((opt, i) => {
                                return (
                                    <MenuItem
                                        key={i}
                                        value={opt.value.join(';')}
                                    >
                                        {opt.name}
                                    </MenuItem>
                                )
                            })
                        }
                    </Select>
                </CollapsedBlock>
            </Box>
        </div>
    );
};
