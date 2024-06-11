import {useDispatch, useSelector} from "react-redux";

import {configureStore} from '@reduxjs/toolkit'
import {apiBase} from "@src/shared/api/apiBase";
import {menuReducer} from "@src/widgets/menuWrapper/store";

import type {TypedUseSelectorHook} from "react-redux";

export const store = configureStore({
    reducer: {
        [apiBase.reducerPath]: apiBase.reducer,
        menu: menuReducer
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(apiBase.middleware),
    devTools: !import.meta.env.PROD,
})

export type RootState = ReturnType<typeof store.getState>

export type AppDispatch = typeof store.dispatch

export const useAppDispatch: () => AppDispatch = useDispatch
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector