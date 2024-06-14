import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";

import {ConsumerCorrelationsInfo} from "../types/consumerCorrelationsInfo";

export const {useGetConsumersCorrelationsQuery} = apiBase.injectEndpoints({
    endpoints: (build => ({
        getConsumersCorrelations: build.query<ConsumerCorrelationsInfo, string>({
            query: (consumer_stations_id) => ({
                url: OBJ_URL + `/api/v1/obj/obj_view/${consumer_stations_id}`,
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})

apiBase.enhanceEndpoints({
    addTagTypes: ['Consumers'],
    endpoints: {
        useGetConsumersCorrelationsQuery: {
            providesTags: ['Consumers']
        }
    }
})