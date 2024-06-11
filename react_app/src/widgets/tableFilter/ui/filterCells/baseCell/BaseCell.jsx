import PropTypes from "prop-types";

import {TableCell, Grid} from "@mui/material";

import {BASE_CELL_CHILD_NAME} from "../../../const/CellNames";

const BaseCell = ({topic, filterIcon, sx, booleanName, children, isInvisible, ...props}) => {
    // Лишний props нужен на уровне таблицы для дефолтной отрисовки строки
    // если не был передан кастомная верстка с помощью функции getTableBodyLayout
    if (props.keyName)
        delete props.keyName

    return (
        <TableCell {...props} sx={{...sx, px: 0}}>
            <Grid container alignItems='center' justifyContent={props.align} flexWrap='nowrap'
                  sx={{px: '8px', maxWidth: '100%'}}>
                {
                    (children || topic)
                        ? <Grid item
                                sx={{
                                    mr: filterIcon ? 1 : 0,
                                    maxWidth: `calc(${filterIcon ? '100% - 32px' : '100%'})`,
                                    overflow: 'auto',
                                    display: 'flex',
                                    alignItems: 'center',
                                    fontWeight: '400',
                                    fontSize: '16px',
                                    lineHeight: '20px',
                                    letterSpacing: '-0.288px',
                                    color: 'rgb(135, 135, 135)'
                                }}
                        >
                            { isInvisible ? '' : children || topic}
                        </Grid>
                        : null
                }
                {
                    filterIcon &&
                    <Grid item
                          sx={{height: '32px', minWidth: '32px', width: '32px', display: 'flex', alignItems: 'center'}}>
                        {filterIcon}
                    </Grid>
                }
            </Grid>
        </TableCell>
    )
}

BaseCell.customFuncName = BASE_CELL_CHILD_NAME

BaseCell.propTypes = {
    topic: PropTypes.string,
    filterIcon: PropTypes.object,
    sx: PropTypes.object,
}

export {BaseCell}
