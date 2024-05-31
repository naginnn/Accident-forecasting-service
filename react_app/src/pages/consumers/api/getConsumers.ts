import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";
import {type Consumers} from "../types/consumers"
export const enum CriticalStatusName {
    IS_APPROVED = 'Подтвержденный инцидент',
    IS_WARNING = 'Риск возникновения инцидента',
    IS_NO_ACCENDENT = 'Нет инцидента'
}

export const defineCriticalStatus = <T extends Consumers | TransformConsumers>(consumer: T): CriticalStatusName => {
    if (consumer.is_warning && !consumer.is_closed) {
        if (!consumer.is_approved) {
            return CriticalStatusName.IS_WARNING
        } else if (consumer.is_approved) {
             return CriticalStatusName.IS_APPROVED
        }
    }

    return CriticalStatusName.IS_NO_ACCENDENT
}

export type TransformConsumers = Consumers & {critical_status: CriticalStatusName}
export const {useGetConsumersQuery} = apiBase.injectEndpoints({
    endpoints: (build => ({
        getConsumers: build.query<TransformConsumers[], void>({
            query: () => ({
                url: OBJ_URL + `/api/v1/obj/table_view`,
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
            transformResponse(val: Consumers[]) {

                return val.map((el) => {
                    let criticalStatus: CriticalStatusName = defineCriticalStatus(el)

                    return {
                        ...el,
                        critical_status: criticalStatus
                    }
                })
            }
        }),
    })),
    overrideExisting: false
})
