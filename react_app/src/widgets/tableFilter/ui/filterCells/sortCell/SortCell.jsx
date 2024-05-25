import {useMemo} from "react";
import ExpandMoreOutlinedIcon from '@mui/icons-material/ExpandMoreOutlined';
import ExpandLessOutlinedIcon from '@mui/icons-material/ExpandLessOutlined';

import {IconButton} from "@mui/material";

import {SORT_CELL_CHILD_NAME} from "../../../const/CellNames";

import {BaseCell} from "../baseCell/BaseCell";

const SortCell =
    ({
         isDateCell = false,
         keyName,
         topic,
         activeName,
         onToggle,
         sortOrderBy,
         sx,
         onChangePage,
         ...props
     }) => {
        const isActiveSort = useMemo(() => {
            if (activeName === keyName && sortOrderBy)
                return true

            return false
        }, [keyName, activeName, sortOrderBy])

        const getFilterIcon = () => {
            return (
                <IconButton
                    onClick={() => {
                        if (onChangePage) onChangePage(undefined, 0)

                        onToggle(keyName, isDateCell)
                    }}
                    sx={{p: '5px', color: (theme) => isActiveSort ? theme.palette.primary.main : ''}}
                >
                    {
                        (keyName === activeName && sortOrderBy === 'asc')
                            ? <ExpandLessOutlinedIcon/>
                            : <ExpandMoreOutlinedIcon/>
                    }
                </IconButton>
            )
        }

        return (
            <BaseCell
                sx={sx}
                topic={topic}
                filterIcon={getFilterIcon()}
                {...props}
            />
        )
    }

SortCell.customFuncName = SORT_CELL_CHILD_NAME;

export {SortCell};