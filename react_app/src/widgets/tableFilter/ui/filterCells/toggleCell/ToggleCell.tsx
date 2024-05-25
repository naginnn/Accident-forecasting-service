import {useEffect, useState} from "react";

import {SxProps, Theme} from '@mui/material/styles';

import {TableCell, Box} from "@mui/material";

import {SessionStorageManager} from "../../../utils/sessionStorageManager";
import {TOGGLE_CELL_CHILD_NAME} from "../../../const/CellNames";

interface ToggleCellProps {
    topic: string;
    data: [];
    keyName: string;
    onFilter: Function;
    tableId?: string
    sx?: SxProps<Theme>

    [x: string]: any;
}

// Сортирует таблицу по значению true / false
const ToggleCell = ({topic, data, keyName, onFilter, tableId, sx, ...props}: ToggleCellProps) => {

    const [isChecked, setIsChecked] = useState<boolean>(() => {
        const prevSelectedOpt = SessionStorageManager.getSelectCellValue(tableId, keyName).join(';')

        return prevSelectedOpt ? JSON.parse(prevSelectedOpt) : false
    })

    useEffect(() => {
        const option = isChecked ? [isChecked] : [];

        onFilter(keyName, option)
    }, [isChecked])

    const onChangeSelectOpt = () => {
        SessionStorageManager.setSelectCellValue(tableId, keyName, [`${!isChecked}`])
        setIsChecked(prev => !prev)
    }

    return (
        <TableCell
            sx={{...sx}}
            {...props}
        >
            <Box
                onClick={onChangeSelectOpt}
                sx={{
                    p: '6px 8px',
                    m: 0,
                    borderRadius: '4px',
                    border: isChecked ? '' : '1px solid #cecece',
                    alignItems: 'center',
                    display: 'flex',
                    height: '40px',
                    color: isChecked ? '#ffffff' : 'black',
                    backgroundColor: isChecked ? '#1976d2' : '#ffffff',
                    '&:hover': {
                        cursor: 'pointer',
                        backgroundColor: isChecked ? '#adcbea' : '#f5f5f5',
                    },
                    wordBreak: 'break-word',
                }}
            >
                <p style={{
                    width: '100%',
                    transform: 'all .6s ease-in-out',
                    letterSpacing: '0.01071rem',
                    fontWeight: '500',
                    fontSize: '0.875rem',
                    lineHeight: '1.5rem',
                }}
                >
                    {topic}
                </p>
            </Box>
        </TableCell>
    )
}

ToggleCell.customFuncName = TOGGLE_CELL_CHILD_NAME;

export {ToggleCell}