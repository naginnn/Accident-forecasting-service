import {apiBase, OBJ_URL, getAuthHeader, getRequestOptions, handleErrorResponse} from "@src/shared/api/apiBase";

import {ConsumerCorrelationsInfo} from "../types/consumerCorrelationsInfo";
import {CriticalStatusName, FormattedConsumer} from "../types/formattedConsumer";

export type FormattedConsumerCorrelationsInfo = Omit<ConsumerCorrelationsInfo, 'consumers_dep'> & {
    consumers_dep: FormattedConsumer[] | null
}

export const {useGetConsumersCorrelationsQuery} = apiBase.injectEndpoints({
    endpoints: (build => ({
        getConsumersCorrelations: build.query<FormattedConsumerCorrelationsInfo, string>({
            query: (consumer_stations_id) => ({
                url: OBJ_URL + `/api/v1/obj/obj_view/${consumer_stations_id}`,
                ...getRequestOptions(getAuthHeader())
            }),
            transformErrorResponse: handleErrorResponse,
            transformResponse(val: ConsumerCorrelationsInfo) {
                let depConsumers: FormattedConsumer[] | null = null

                if (val.consumers_dep) {
                    depConsumers = val.consumers_dep.map(info => {
                        let criticalStatus = CriticalStatusName["IS_NO_ACCENDENT"]

                        if (info.events?.length && !info.events[0].is_closed) {
                            if (info.events[0].is_approved) {
                                criticalStatus = CriticalStatusName.IS_APPROVED
                            } else {
                                criticalStatus = CriticalStatusName.IS_WARNING
                            }
                        }
                        return {
                            ...info,
                            critical_status: criticalStatus
                        }
                    })
                }

                return {
                    ...val,
                    consumers_dep: depConsumers
                }
            }
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