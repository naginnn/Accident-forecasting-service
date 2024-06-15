import {Consumer} from "./consumerCorrelationsInfo";

export const enum CriticalStatusName {
    IS_APPROVED = 'Подтвержденный инцидент',
    IS_WARNING = 'Риск возникновения инцидента',
    IS_NO_ACCENDENT = 'Нет инцидента'
}

export type FormattedConsumer = Consumer & {
    critical_status: CriticalStatusName
}