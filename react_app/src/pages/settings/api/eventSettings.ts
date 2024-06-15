import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";
import {EventSetting} from "../types/EventSetting";

export const {
    useGetEventsSettingQuery,
    useDeleteEventSettingMutation,
    useAddEventSettingMutation
} = apiBase.injectEndpoints({
    endpoints: (build => ({
        getEventsSetting: build.query<EventSetting[], void>({
            query: () => ({
                url: OBJ_URL + `/api/v1/obj/config/events`,
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
        deleteEventSetting: build.mutation<EventSetting[], number>({
            query: (id) => ({
                url: OBJ_URL + `/api/v1/obj/config/events/${id}`,
                ...getRequestOptions(getAuthHeader()),
                method: 'DELETE'
            }),
            transformErrorResponse: handleErrorResponse,
        }),
        addEventSetting: build.mutation<unknown, EventSetting>({
            query: (event) => ({
                url: OBJ_URL + `/api/v1/obj/config/events`,
                ...getRequestOptions(getAuthHeader()),
                body: JSON.stringify(event),
                method: 'POST'
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})

apiBase.enhanceEndpoints({
    addTagTypes: ['EventsSetting'],
    endpoints: {
        useGetEventsQuery: {
            providesTags: ['EventsSetting']
        },
        useDeleteEventSettingMutation: {
            invalidatesTags: ['EventsSetting']
        },
        useAddEventSettingMutation: {
            invalidatesTags: ['EventsSetting']
        }
    }
})
