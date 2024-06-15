import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";
import {CounterEvent} from "../types/counterEvents";


export const {useGetCounterEventsQuery} = apiBase.injectEndpoints({
    endpoints: (build => ({
        getCounterEvents: build.query<CounterEvent[], number>({
            query: (consumer_id) => ({
                url: OBJ_URL + `/api/v1/obj/events_counter/${consumer_id}`,
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})
