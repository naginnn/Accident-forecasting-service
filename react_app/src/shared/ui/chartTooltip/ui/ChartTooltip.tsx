import {Paper, Typography} from "@mui/material";

/*
    Компонент отображение подсказки на графике

    props - принимает в себя все пропсы компонента
    Tooltip из библиотеки recharts, но испол-ся только payload, label, formatter
*/
export const ChartTooltip = (props: any) => {
    const {payload, label, formatter} = props

    if (!payload)
        return null

    // Разворачиваем массив чтобы порядок линий переданных в компонент графика
    // соответствовал порядку строк на Tooltip
    const reversedPayload = payload.reverse()

    return (
        <Paper sx={{p: '20px', display: 'flex', flexDirection: 'column', border: 'none'}}>
            <Typography fontWeight={500}>{label}</Typography>
            {
                reversedPayload.map((el: any, i: number) => {
                    return (
                        <Typography
                            key={i}
                            fontWeight={500}
                            color={el.stroke}
                        >
                            {
                                formatter && typeof formatter === 'function'
                                    ? `${formatter(el.payload[el.dataKey], el.dataKey)[1]}: ${formatter(el.payload[el.dataKey], el.dataKey)[0]}`
                                    : <>
                                        {el.name}: &nbsp;
                                        {
                                            typeof el.dataKey === 'function'
                                                ? el.dataKey(el.payload)
                                                : el.payload[el.dataKey]
                                        }
                                        {el.unit}
                                    </>
                            }
                        </Typography>
                    )
                })
            }
        </Paper>
    )
}