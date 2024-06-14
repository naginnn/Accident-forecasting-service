import {useEffect, useState} from "react";
import {ReferenceArea} from "recharts";


// Hook отвечающий за zoom графика
// data - массив точек для отрисовки графика
export const useHightlightChart = (data = []) => {
    const [slicedData, setSlicedData] = useState(data) // отзумленная дата

    const [areaIndex, setAreaIndex] = useState({left: undefined, right: undefined});
    const [areaXAxisData, setAreaXAxisData] = useState({left: undefined, right: undefined});

    // Сброс границ области выделения
    const resetBorder = () => {
        setAreaIndex({left: undefined, right: undefined});
        setAreaXAxisData({left: undefined, right: undefined})
    }

    // При изменении data сбрасывает границы и инициализирует отзумленную дата
    useEffect(() => {
        resetBorder()
        setSlicedData(data);
    }, [data])

    const zoom = () => {
        if (areaIndex.left === areaIndex.right
            || areaIndex.right === undefined
            || areaIndex.left === undefined) {
            resetBorder()

            return;
        }

        // Выявление реальной левой и правой границы
        const leftArea = Math.min(areaIndex.left, areaIndex.right)
        const rightArea = Math.max(areaIndex.left, areaIndex.right)

        setSlicedData(slicedData.slice(leftArea, rightArea + 1));
        resetBorder()
    }

    // Выход из зума
    const zoomOut = () => {
        resetBorder()

        setSlicedData(data);
    }

    const setLeftBorder = (e) => {
        if (e) {
            setAreaIndex({...areaIndex, left: e.activeTooltipIndex})
            setAreaXAxisData({...areaIndex, left: e.activeLabel})
        }
    }

    const setRightBorder = (e) => {
        if (e) {
            areaIndex.left !== undefined && setAreaIndex({...areaIndex, right: e.activeTooltipIndex})
            areaXAxisData.left !== undefined && setAreaXAxisData({...areaXAxisData, right: e.activeLabel})
        }
    }

    //Возвращает облатсь выделение есть установленый границы
    const getReferenceArea = () => {
        return (
            areaXAxisData.left && areaXAxisData.right
                ? <ReferenceArea ifOverflow='hidden' x1={areaXAxisData.left} x2={areaXAxisData.right} strokeOpacity={0.3}/>
                : null
        )
    }

    return ({slicedData, setLeftBorder, setRightBorder, zoom, zoomOut, getReferenceArea})
}
