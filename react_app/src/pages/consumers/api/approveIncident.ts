import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";
export const {useApproveIncidentMutation} = apiBase.injectEndpoints({
    endpoints: (build => ({
        approveIncident: build.mutation<void, number>({
            query: (consumerId) => ({
                url: OBJ_URL + `/api/v1/obj/events?id=${consumerId}&cmd=approve`,
                method: 'POST',
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})
