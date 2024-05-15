import {apiBase, getAuthHeader, getRequestOptions, handleErrorResponse, OBJ_URL} from "@src/shared/api/apiBase";

export const {useGetAreasQuery} = apiBase.injectEndpoints({
    endpoints: (build => ({
        getAreas: build.query<void, void>({
            query: () => ({
                url: OBJ_URL + `/api/v1/obj/areas`,
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})
