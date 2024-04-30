import {apiBase, AUTH_URL, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";

export const {useRegistrationMutation} = apiBase.injectEndpoints({
    endpoints: (build => ({
        registration: build.mutation<string, { login: string, password: string, roles: string }>({
            query: ({login, password, roles}) => ({
                url: AUTH_URL + `/api/v1/auth/token`,
                ...getRequestOptions({
                    'Content-Type':	'application/json; charset=utf-8'
                }),
                body: JSON.stringify({
                    roles,
                    cred: btoa(`${login}:${password}`),
                }),
                method: 'POST'
            }),
            transformErrorResponse: handleErrorResponse,
            transformResponse(val: { tkn: string }) {
                return val.tkn
            }
        }),
    })),
    overrideExisting: false
})
