import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";

import {ConsumerCorrelationsInfo} from "../types/consumerCorrelationsInfo";

export const {useLazyGetConsumerQuery} = apiBase.injectEndpoints({
    endpoints: (build => ({
        getConsumer: build.query<ConsumerCorrelationsInfo, number>({
            query: (consumer_id) => ({
                url: OBJ_URL + `/api/v1/obj/objects/consumers/${consumer_id}`,
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
        useGetConsumerQuery: {
            providesTags: ['Consumers']
        }
    }
})