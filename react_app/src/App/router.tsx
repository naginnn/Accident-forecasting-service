import {createBrowserRouter} from "react-router-dom";

import {PrivateRoute} from "./PrivateRoute";

import {Login} from "../pages/login";
// import {Registration} from "../pages/registration";
import {OutOfRange} from "../pages/outOfRange";


// Пути страничек
const router = createBrowserRouter([
    {
        path: "/",
        element: <PrivateRoute/>,
        errorElement: <div>ERROR</div>,
        children: [
        ]
    },
    // {
    //     path: '/registration',
    //     element: <Registration/>
    // },
    {
        path: '/login',
        element: <Login/>
    },
    {
        path: '*',
        element: <OutOfRange/>
    },
]);

export default router;