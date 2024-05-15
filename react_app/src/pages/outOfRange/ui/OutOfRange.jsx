import {useNavigate} from "react-router-dom";
import {useEffect} from "react";
import {YMap} from "@src/widgets/YMap";

// Компонент обработки по переходу несуществующего пути
export const OutOfRange = () => {
    const navigate = useNavigate()

    // useEffect(() => {
    //     navigate('/')
    // }, [])

    return (
        <>
            <div>PAGE DOESN'T EXIST</div>
        </>
    )
}