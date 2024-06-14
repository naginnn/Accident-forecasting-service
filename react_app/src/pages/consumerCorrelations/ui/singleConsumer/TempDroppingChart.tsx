import dayjs from "dayjs";
import {FC, useMemo} from "react";

import {AreaChart, Tooltip, YAxis, XAxis, Area, CartesianGrid} from "recharts";

import {useChartView} from "@src/shared/hooks/useChartView";
import {useHightlightChart} from "@src/shared/hooks/useHightlightChart";
import {AreaChartWrapper} from "@src/entities/areaChartWrapper";
import {ChartTooltip} from "@src/shared/ui/chartTooltip";

import {TempDropping} from "../../types/consumerCorrelationsInfo";

interface TempDroppingChartProps {
    data: TempDropping[]
}

export const TempDroppingChart: FC<TempDroppingChartProps> = ({data}) => {
    const formattedData = useMemo(() => {

        return data.map(el => {
            return {
                'Температура': typeof el.temp === 'number' ? +el.temp.toFixed(0) : 0,
                'Дата': dayjs.unix(el.date_ts).format('DD.MM HH:mm')
            }
        })
    }, [data])


    //@ts-nocheck
    const {
        slicedData,
        setLeftBorder,
        setRightBorder,
        zoom,
        zoomOut,
        getReferenceArea,
    } = useHightlightChart(formattedData)
    const {showCartesianGrid} = useChartView(formattedData, 90);

    return (
        <AreaChartWrapper
            height={410}
            chartTopic=''
            handleZoomOut={zoomOut}
        >
            <AreaChart
                margin={{top: 20, bottom: 60, right: 10}}
                data={slicedData}
                onMouseDown={setLeftBorder}
                onMouseMove={setRightBorder}
                onMouseUp={zoom}
            >
                {showCartesianGrid && <CartesianGrid strokeDasharray="3 3"/>}
                <XAxis dataKey='Дата' angle={-70} tickMargin={40}/>
                <YAxis unit=' °C' dataKey='Температура' domain={[0, 50]}/>
                <Tooltip content={<ChartTooltip/>} formatter={(value, name) => ([`${value} °C`, name])}/>
                <Area
                    type="monotone"
                    dataKey="Температура"
                    stroke='#1e88e5'
                    fillOpacity={0}
                    strokeWidth={2}
                />
                {getReferenceArea()}
            </AreaChart>
        </AreaChartWrapper>
    );
};
