import { v4 as uuidv4 } from 'uuid';
import {BaseQueryFn, createApi, FetchArgs, fetchBaseQuery, FetchBaseQueryError} from "@reduxjs/toolkit/query/react";

const baseQuery = fetchBaseQuery({baseUrl: ''})

const baseQueryWithRequesId: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (args, api, extraOptions) => {
    let result = await baseQuery(args, api, extraOptions)
    let requestId = uuidv4()

    return {
        ...result,
        meta: result.meta && {...result.meta, requestId}
    }
}

export const apiBase = createApi({
    baseQuery: baseQueryWithRequesId,
    endpoints: () => ({}),
    refetchOnReconnect: true,
    refetchOnMountOrArgChange: true,
})