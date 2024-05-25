import {useDeferredValue, useEffect, useMemo, useState} from "react";

import MoreVertIcon from "@mui/icons-material/MoreVert";
import {Checkbox, MenuItem, Box, MenuList, Typography, useTheme} from "@mui/material";

import {SearchInput} from "@src/shared/ui/searchInput";
import {IconButtonWithPopover} from "@src/entities/iconButtonWithPopover";

import {ALL_OPTIONS_NAME} from "./SelectCell";

interface IOptionsProps {
    options: string[]
    selectedOptions: string[]
    booleanName: [string, string] | undefined
    onChangeSelectOptions: (option: string) => void
}

export const Options = ({options, selectedOptions, booleanName, onChangeSelectOptions}: IOptionsProps) => {
    const [searchedOptions, setSearchedOptions] = useState<Array<string>>(options)
    const [searchValue, setSearchValue] = useState<string>('');
    const deferredFilterSearch = useDeferredValue(searchValue);
    const {palette} =  useTheme()

    useEffect(() => {
        setSearchedOptions(options)
    }, [options])

    useEffect(() => {
        const filterLowCase = searchValue.toLowerCase().trim();

        const filteredOptions = options.filter(option => option.toLowerCase().includes(filterLowCase))
        const withAllSelect = filteredOptions.some(option => option === ALL_OPTIONS_NAME)

        setSearchedOptions(() => withAllSelect ? filteredOptions : [ALL_OPTIONS_NAME, ...filteredOptions])
    }, [deferredFilterSearch])

    const onSearchInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchValue(e.target.value)
    }

    const isAllSelected: boolean = useMemo(() => {
        if (!selectedOptions.length || selectedOptions.length === options.length)
            return true

        return false
    }, [selectedOptions, options])

    return (
       <IconButtonWithPopover
           buttonIcon={<MoreVertIcon/>}
           buttonSx={(() => {
               if (isAllSelected) return {}
               return {color: palette.primary.main}
           })()}
       >
           <>
               {
                   !booleanName &&
                   <Box sx={{display: 'flex', justifyContent: 'center', my: '10px'}}>
                       <SearchInput
                           sx={{minWidth: '90%', maxWidth: '90%'}}
                           value={searchValue}
                           onChange={onSearchInput}
                       />
                   </Box>
               }
               <MenuList sx={{p: 0, maxWidth: '400px'}}>
                   {
                       searchedOptions.map(option =>
                           <Option
                               option={option}
                               selectedOptions={selectedOptions}
                               booleanName={booleanName}
                               onChangeSelectOptions={onChangeSelectOptions}
                               key={option}
                           />
                       )
                   }
               </MenuList>
           </>
       </IconButtonWithPopover>
    )
}

interface IOptionProps {
    option: string
    selectedOptions: Array<string>
    booleanName: [string, string] | undefined
    onChangeSelectOptions: (option: string) => void
}

const Option = ({option, selectedOptions, booleanName, onChangeSelectOptions}: IOptionProps) => {
    const isChecked = !!~selectedOptions.findIndex((selectedOpt) => option === selectedOpt)
    let optionName = option

    if ((option === 'false' || option === 'true') && booleanName) {
        if (booleanName.length !== 2)
            throw new Error('Нет данных для переименования параметров ячейки')

        optionName = option === 'true' ? booleanName[0] : booleanName[1]
    }

    return (
        <MenuItem onClick={() => onChangeSelectOptions(option)}>
            <Checkbox
                checked={isChecked}
                disableRipple
                size='small'
            />
            <Typography sx={{maxWidth: '330px', wordBreak: 'break-word', whiteSpace: 'pre-line'}}>
                {optionName}
            </Typography>
        </MenuItem>
    )
}