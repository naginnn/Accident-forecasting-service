import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";
import {ModelInfo} from "../types/modelInfo";

export const {
    useGetModelInfoQuery,
} = apiBase.injectEndpoints({
    endpoints: (build => ({
        getModelInfo: build.query<ModelInfo, void>({
            query: () => ({
                url: OBJ_URL + `/api/v1/obj/analytics/model_info`,
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
        }),
    })),
    overrideExisting: false
})
