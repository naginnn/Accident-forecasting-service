import {useEffect, useState} from "react";

// Hook которые возвращает boolean значение отвечающее
// за отрисовку сетки для графиков


// data - массив точек для отрисовки графика
// cartesianViewLimit - пограничное значение для отрисовки сетки
// P.S. можно было просто использовать useMemo
export const useChartView = (data: any[], cartesianViewLimit: number) => {
    const [showCartesianGrid, setShowCartesianGrid] = useState(false)

    if (cartesianViewLimit < 0) {
        throw new Error('Число для отрисовки сетки должно быть больше нуля')
    }

    useEffect(() => {
        setShowCartesianGrid(data.length > cartesianViewLimit ? false : true);
    }, [data, cartesianViewLimit])

    return {showCartesianGrid}
}
