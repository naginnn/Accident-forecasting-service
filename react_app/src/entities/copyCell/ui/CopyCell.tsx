import {FC} from "react";

import {Box, SxProps, TableCell, Theme} from "@mui/material";
import {TableCellProps} from "@mui/material/TableCell/TableCell";

import {CopyClickBoardBtn} from "@src/shared/ui/copyClickBoardBtn";

interface ICopyCellProps {
    sx?: SxProps<Theme>
    tableCellProps?: TableCellProps
    children: string | number | boolean
}

/*
    Ячейка с возможностью копирования текста

    sx - стили для ячейки обертки
    tableCellProps - стили для ячейки
    children - текст для копирования/отображения
*/
export const CopyCell: FC<ICopyCellProps> = ({children, sx = {}, tableCellProps = {}}) => {
    return <TableCell {...tableCellProps}>
        <Box sx={{display: 'flex', alignItems: 'center', gap: '8px', ...sx}}>
            <CopyClickBoardBtn
                text={children.toString()}
                sx={{width: '17px', height: '17px'}}
            />
            <Box>
                {children.toString()}
            </Box>
        </Box>
    </TableCell>
}