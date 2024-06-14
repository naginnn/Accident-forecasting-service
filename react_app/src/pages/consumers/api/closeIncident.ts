import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";

export const {useCloseIncidentMutation} = apiBase.injectEndpoints({
    endpoints: (build => ({
        closeIncident: build.mutation<void, number>({
            query: (eventId) => ({
                url: OBJ_URL + `/api/v1/obj/events?id=${eventId}&cmd=close`,
                method: 'POST',
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})
