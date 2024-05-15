import {apiBase, AUTH_URL, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";

export const {useLazyLoginQuery} = apiBase.injectEndpoints({
    endpoints: (build => ({
        login: build.query<string, { login: string, password: string }>({
            query: ({login, password}) => ({
                url: AUTH_URL + `/api/v1/auth/token`,
                ...getRequestOptions({
                    Authorization: 'Basic ' + btoa(`${login}:${password}`)
                })
            }),
            transformErrorResponse: handleErrorResponse,
            transformResponse(val: { tkn: string }) {
                return val.tkn
            }
        }),
    })),
    overrideExisting: false
})
