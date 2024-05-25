import {useMemo} from "react";

import FilterAltIcon from "@mui/icons-material/FilterAlt";

import {Checkbox, MenuItem, MenuList, useTheme} from "@mui/material";

import {IconButtonWithPopover} from "@src/entities/iconButtonWithPopover";

interface ICellsProps {
    keyName?: string
    topic?: string
    id?: number

    [x: string]: any
}

interface IManageColumnButtonProps {
    cellsProps: Array<ICellsProps>
    visibleColumn: { [x: string]: boolean }
    onToggleAllColumn: (val: boolean) => void
    onToggleColumn: (id: number) => void
}

export const ManageColumnButton = (
    {
        cellsProps,
        visibleColumn,
        onToggleColumn,
        onToggleAllColumn
    }: IManageColumnButtonProps) => {
    const {palette} = useTheme()

    const isAllSelected = useMemo(() => {
        return Object.values(visibleColumn).every(val => val)
    }, [visibleColumn])

    return (
        <IconButtonWithPopover
            buttonSx={(() => {
                if (isAllSelected) return {}
                return {color: palette.primary.main}
            })()}
            anchorOrigin={{vertical: 'bottom', horizontal: 'left'}}
            transformOrigin={{vertical: 'top', horizontal: 'right'}}
            PaperProps={{
                style: {
                    minHeight: '40px',
                    maxHeight: '300px',
                    minWidth: '200px',
                    width: 'max-content',
                },
            }}
            buttonIcon={<FilterAltIcon/>}
        >
            <MenuList sx={{p: 0}}>
                <MenuItem onClick={() => onToggleAllColumn(!isAllSelected)}>
                    <Checkbox
                        checked={isAllSelected}
                        disableRipple
                        size='small'
                    />
                    Все
                </MenuItem> {
                cellsProps.map(({keyName, id, topic}, i) => {
                    if (!id)
                        throw new Error(`Не передан id в ячейку ${topic} - ${keyName}`)
                    return (
                        <Option
                            keyName={keyName}
                            id={id}
                            topic={topic}
                            isSelected={visibleColumn[id]}
                            onSelected={onToggleColumn}
                            key={i}
                        />
                    )
                })
            }
            </MenuList>
        </IconButtonWithPopover>
    )
}

interface IOption {
    id: number
    keyName?: string
    topic?: string
    onSelected: (keyNames: number) => void
    isSelected: boolean
}

const Option = ({id, keyName, topic, isSelected, onSelected}: IOption) => {
    if (!topic)
        console.error(`Не передано имя ячейки в столбе ${keyName}`)

    return (
        <MenuItem onClick={() => onSelected(id)}>
            <Checkbox
                checked={isSelected}
                disableRipple
                size='small'
            />
            {topic || keyName}
        </MenuItem>
    )
}