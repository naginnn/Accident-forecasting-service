import {useDownloadFile} from "@src/features/useDownloadFile";
import {getAuthHeader} from "@src/shared/api/apiBase";
import {REPORT_URL} from "@src/shared/api/apiBase/const/urls";

export const useDownloadConsumer = () => {
    const {downloadFile: externalDowloadExcel, isLoading, error, isSuccess} = useDownloadFile();

    const downloadExcel = (id: number) => {
        externalDowloadExcel(REPORT_URL + `/api/v1/predict/objects_report/${id}`, getAuthHeader())
    }

    return {downloadExcel, isLoading, error, isSuccess}
}

export const useDownloadConsumerStation = () => {
    const {downloadFile: externalDowloadExcel, isLoading, error, isSuccess} = useDownloadFile();

    const downloadExcel = (id: number) => {
        externalDowloadExcel(REPORT_URL + `/api/v1/predict/con_station_report/${id}`, getAuthHeader())
    }

    return {downloadExcel, isLoading, error, isSuccess}
}