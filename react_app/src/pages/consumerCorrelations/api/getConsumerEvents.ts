import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";
import {EventConsumer} from "../types/consumerCorrelationsInfo";

export const {useGetConsumerEventsQuery} = apiBase.injectEndpoints({
    endpoints: (build => ({
        getConsumerEvents: build.query<EventConsumer[], string>({
            query: (consumer_id) => ({
                url: OBJ_URL + `/api/v1/obj/events/${consumer_id}`,
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})
