import TableRow from "@mui/material/TableRow";

import {SxProps, Theme} from "@mui/material/styles";

interface IFocusedTableRowProps {
    sx?: SxProps<Theme>
    children: any

    [x: string]: any
}

export const FocusedTableRow = ({children, sx = {}, ...props}: IFocusedTableRowProps) => {
    return (
        <TableRow
            sx={{
                '&:hover': {cursor: 'pointer', bgcolor: '#f5f5f5'},
                ...(Array.isArray(sx) ? sx : [sx])
            }}
            {...props}
        >
            {children}
        </TableRow>
    );
}