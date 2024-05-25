import {TableBody, TableCell, TableRow} from "@mui/material";

export const DefaultTableBody = ({data, cellProps, getPageContent, visibleColumn}) => {
    return (
        <TableBody>
            {
                getPageContent(data).map((row, i) => {
                    return (
                        <TableRow key={i}>
                            {
                                cellProps.map(props => {
                                    let value = row[props.keyName]

                                    if (visibleColumn && props.id in visibleColumn && !visibleColumn[props.id])
                                        return null

                                    if (typeof value === 'boolean') {
                                        if (props.booleanName && props.booleanName.length === 2)  {
                                            value = value ? props.booleanName[0] : props.booleanName[1]
                                        } else {
                                            value = ''
                                        }

                                    } else if (typeof value === 'object') {
                                        value = ''
                                    }

                                    return (
                                        <TableCell key={props.keyName} align={props.align}>
                                            {value}
                                        </TableCell>
                                    )
                                })
                            }
                        </TableRow>
                    )
                })
            }
        </TableBody>
    )
}