import {useToggle} from "@src/shared/hooks/useToggle";

import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";

import {Divider, Grid, Tooltip, Box, Typography, useTheme} from "@mui/material";

import {SxProps, Theme} from "@mui/material/styles";
import {TooltipProps} from "@mui/material/Tooltip/Tooltip";

interface ICollapsedBlock {
    topicName: string
    children: any
    tooltipHeader?: string
    tooltipHeaderPlacement?: TooltipProps['placement']
    withDivider?: boolean
    textPlacement?: 'right' | 'left'
    isOpenInit?: boolean
    onOpen?: () => void
    sideComponent?: React.ReactNode
    sx?: SxProps<Theme>
}

// Если не передана функция для изменения состоянием открытия
// и информация об открытости - закрытия, то реализует собственный механизм открыти - закрытия
// на основе локальных стейтов
export const CollapsedBlock = (
    {
        children,
        topicName,
        isOpenInit = false,
        onOpen,
        tooltipHeader,
        tooltipHeaderPlacement = 'left',
        textPlacement = 'left',
        withDivider = false,
        sideComponent = null
    }: ICollapsedBlock) => {
    const {value: isOpenIternal, toggle: onToggleInternal} = useToggle(isOpenInit)

    const handleToggle = () => {
        if (typeof isOpenInit === 'boolean' && onOpen && typeof onOpen === 'function') {
            onOpen()
        } else {
            onToggleInternal()
        }
    }

    const getDivider = () => {
        return (
            <Grid container columnSpacing={2} item xs alignItems='center'>
                {
                    textPlacement === 'left'
                        ? <>
                            <Grid item xs>
                                {
                                    withDivider && <Divider/>
                                }
                            </Grid>
                            <Grid item xs='auto'>
                                {sideComponent}
                            </Grid>
                        </>
                        : <>
                            <Grid item xs='auto'>
                                {sideComponent}
                            </Grid>
                            <Grid item xs>
                                {
                                    withDivider && <Divider/>
                                }
                            </Grid>
                        </>
                }
            </Grid>
        )
    }

    return (
        <>
            <Tooltip title={tooltipHeader} placement={tooltipHeaderPlacement}>
                <Grid container columnSpacing={2} alignItems='center' justifyContent='space-between'>
                    {textPlacement === 'right' && getDivider()}
                    <Grid container columnSpacing={2} item xs='auto'
                          onClick={handleToggle}
                          sx={{
                              '&:hover': {
                                  cursor: 'pointer',
                                  color: '#616161'
                              }
                          }}
                    >
                        <Grid item>
                            {
                                isOpenIternal
                                    ? <KeyboardArrowUpIcon/>
                                    : <KeyboardArrowDownIcon/>
                            }
                        </Grid>
                        <Grid item>
                            <Typography sx={{userSelect: 'none'}}>{topicName}</Typography>
                        </Grid>
                    </Grid>
                    {textPlacement === 'left' && getDivider()}
                </Grid>
            </Tooltip>
            {isOpenIternal && children}
        </>
    )
}
