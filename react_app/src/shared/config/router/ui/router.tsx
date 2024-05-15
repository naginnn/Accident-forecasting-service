import {createBrowserRouter, RouteObject} from "react-router-dom";

import {PrivateRoute} from "./PrivateRoute";

import {Login} from "@src/pages/login";
import {Registration} from "@src/pages/registration";
import {OutOfRange} from "@src/pages/outOfRange";

import {YMap} from "@src/widgets/YMap"

export enum AppRoutes {
    LOGIN = 'login',
    REGISTRATION = 'registration',
    NOT_FOUND = 'not_found',
    MAP = 'map'
}

export const routerPaths: Record<AppRoutes, string> = {
    [AppRoutes.LOGIN]: '/login',
    [AppRoutes.REGISTRATION]: '/registration',
    [AppRoutes.NOT_FOUND]: '*',
    [AppRoutes.MAP]: 'map',
}

export const routes: RouteObject[] = [
    {
        path: "/",
        element: <PrivateRoute/>,
        errorElement: <div>ERROR</div>,
        children: [
        ]
    },
    {
        path: routerPaths[AppRoutes.LOGIN],
        element: <Login/>
    },
    {
        path: routerPaths[AppRoutes.REGISTRATION],
        element: <Registration/>
    },
    {
        path: routerPaths[AppRoutes.MAP],
        element: <YMap/>
    },
    {
        path: routerPaths[AppRoutes.NOT_FOUND],
        element: <OutOfRange/>
    }
]

// Пути страничек
export const router = createBrowserRouter(routes);

