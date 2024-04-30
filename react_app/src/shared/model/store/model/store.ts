import {configureStore} from '@reduxjs/toolkit'
import {apiBase} from "@src/shared/api/apiBase";
export const store = configureStore({
    reducer: {
        [apiBase.reducerPath]: apiBase.reducer,
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(apiBase.middleware),
    devTools: !import.meta.env.PROD,
})

export type RootState = ReturnType<typeof store.getState>

export type AppDispatch = typeof store.dispatch