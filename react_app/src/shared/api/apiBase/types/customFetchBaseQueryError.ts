import {FetchBaseQueryError} from "@reduxjs/toolkit/dist/query/react";

export type CustomFetchBaseQueryErrT = FetchBaseQueryError & {
    requestId: string
}