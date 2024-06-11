import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";

export const {useCloseIncidentMutation} = apiBase.injectEndpoints({
    endpoints: (build => ({
        closeIncident: build.mutation<void, number>({
            query: (consumerId) => ({
                url: OBJ_URL + `/api/v1/obj/events?id=${consumerId}&cmd=close`,
                method: 'POST',
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})
