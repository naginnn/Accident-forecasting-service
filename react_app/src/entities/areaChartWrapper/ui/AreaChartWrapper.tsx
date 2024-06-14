import {ReactNode} from "react";

import ZoomOutIcon from "@mui/icons-material/ZoomOut";

import {Grid, Typography, IconButton} from "@mui/material"

import {ResponsiveContainer} from "recharts";

interface IAreaChartWrapperProps {
    height: number
    chartTopic?: string | ReactNode
    handleZoomOut?: () => void
    children: any
}

/*
    Обертка для графиков с заголовком и возможностью zoom
    height - высота графика
    chartTopic - название графика
    children - график
    handleZoomOut - обработчик выхода из зума

    P.S На скриншоте не хватает chartTopic
 */
export const AreaChartWrapper = ({height, chartTopic, handleZoomOut, children}: IAreaChartWrapperProps) => {
    return (
        <>
            <Grid container alignItems='center' justifyContent='space-between'>
                <Grid item>
                    {
                        typeof chartTopic === 'string'
                            ? <Typography fontWeight={500}>{chartTopic}</Typography>
                            : chartTopic
                    }
                </Grid>
                <Grid item>
                    {
                        handleZoomOut &&
                        <IconButton onClick={handleZoomOut}>
                            <ZoomOutIcon/>
                        </IconButton>
                    }
                </Grid>
            </Grid>
            <ResponsiveContainer width='100%' height={height}>
                {children}
            </ResponsiveContainer>
        </>
    )
}