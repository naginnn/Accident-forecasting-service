import {useEffect, useState} from "react";

interface IScreenSize {
    width: number // ширина окна window
    height: number // высота окна window
}

export const useWindowSize = () => {
    const [screenSize, setScreenSize] = useState<IScreenSize>(() => ({
        width: window?.innerWidth || 1200,
        height: window?.innerHeight || 800
    }))

    const changeScreenSize = () => {
        setScreenSize({
            width: window?.innerWidth || 1200,
            height: window?.innerHeight || 800
        })
    }

    useEffect(() => {
        // Добавление слушателя на изменение размера window
        window.addEventListener("resize", changeScreenSize);

        return () => {
            // Удаление слушателя
            window.removeEventListener("resize", changeScreenSize)
        }
    }, [])

    return screenSize
}