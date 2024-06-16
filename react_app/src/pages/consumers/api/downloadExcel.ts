import {useDownloadFile} from "@src/features/useDownloadFile";
import {getAuthHeader, REPORT_URL} from "@src/shared/api/apiBase";

export const useDownloadConsumers = () => {
    const {downloadFile: externalDowloadExcel, isLoading, error, isSuccess} = useDownloadFile();

    const downloadExcel = () => {
        externalDowloadExcel(REPORT_URL + `/api/v1/predict/objects_report`, getAuthHeader())
    }

    return {downloadExcel, isLoading, error, isSuccess}
}