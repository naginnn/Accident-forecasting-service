import {defineCriticalStatus, TransformConsumers} from "../api/getConsumers";

export const manageConsumerStatus = (
    data: TransformConsumers[],
    consumerId: number,
    keyName: keyof Pick<TransformConsumers, 'is_approved' | 'is_closed' | 'is_warning'>,
    val: boolean
) => {
    return data.map(consumer => {
        if (consumer.consumer_id === consumerId) {
            const updatedConsumer = {

            }

            return {
                ...consumer,
                [keyName]: val,
                critical_status: defineCriticalStatus({
                    ...consumer,
                    [keyName]: val,
                })
            }
        }
        return consumer
    })
}