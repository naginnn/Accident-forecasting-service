import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";
export const {useApproveIncidentMutation} = apiBase.injectEndpoints({
    endpoints: (build => ({
        approveIncident: build.mutation<void, number>({
            query: (eventId) => ({
                url: OBJ_URL + `/api/v1/obj/events?id=${eventId}&cmd=approve`,
                method: 'POST',
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})
