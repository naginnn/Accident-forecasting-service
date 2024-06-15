import {createBrowserRouter, RouteObject} from "react-router-dom";

import {PrivateRoute} from "./PrivateRoute";

import {Login} from "@src/pages/login";
import {Registration} from "@src/pages/registration";
import {OutOfRange} from "@src/pages/outOfRange";
import {ErrorLayout} from "@src/entities/errorWrapper";

import {Consumers} from "src/pages/consumers";
import {ConsumerCorrelations} from "@src/pages/consumerCorrelations";
import {Settings} from "@src/pages/settings";
import {ModelInfo} from "@src/pages/modelInfo";

export enum AppRoutes {
    LOGIN = 'login',
    REGISTRATION = 'registration',
    NOT_FOUND = 'not_found',
    CONSUMERS = 'consumers',
    CONSUMERS_CORRELATIONS = 'consumers_correlations',
    SETTINGS = 'settings',
    MODEL_INFO = 'model-info'
}

export const routerPaths: Record<AppRoutes, string> = {
    [AppRoutes.LOGIN]: '/login',
    [AppRoutes.REGISTRATION]: '/registration',
    [AppRoutes.NOT_FOUND]: '*',
    [AppRoutes.CONSUMERS]: '/consumers',
    [AppRoutes.CONSUMERS_CORRELATIONS]: '/consumers/:consumer_stations_id',
    [AppRoutes.SETTINGS]: '/settings',
    [AppRoutes.MODEL_INFO]: '/model-info'
}

export const routes: RouteObject[] = [
    {
        path: "/",
        element: <PrivateRoute/>,
        errorElement: <ErrorLayout/>,
        children: [
            {
                path: routerPaths[AppRoutes.CONSUMERS],
                element: <Consumers/>,
                errorElement: <ErrorLayout/>
            },
            {
                path: routerPaths[AppRoutes.CONSUMERS_CORRELATIONS],
                element: <ConsumerCorrelations/>,
                errorElement: <ErrorLayout/>
            },
            {
                path: routerPaths[AppRoutes.SETTINGS],
                element: <Settings/>,
                errorElement: <ErrorLayout/>
            },
            {
                path: routerPaths[AppRoutes.MODEL_INFO],
                element: <ModelInfo/>,
                errorElement: <ErrorLayout/>
            }
        ]
    },
    {
        path: routerPaths[AppRoutes.LOGIN],
        element: <Login/>,
        errorElement: <ErrorLayout/>
    },
    {
        path: routerPaths[AppRoutes.REGISTRATION],
        element: <Registration/>,
        errorElement: <ErrorLayout/>
    },
    {
        path: routerPaths[AppRoutes.NOT_FOUND],
        element: <OutOfRange/>,
        errorElement: <ErrorLayout/>
    }
]

// Пути страничек
export const router = createBrowserRouter(routes);

