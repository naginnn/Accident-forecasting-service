import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";

export const {useCancelIncidentMutation} = apiBase.injectEndpoints({
    endpoints: (build => ({
        cancelIncident: build.mutation<void, number>({
            query: (consumerId) => ({
                url: OBJ_URL + `/api/v1/obj/events?id=${consumerId}&cmd=cancel`,
                method: 'POST',
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})
