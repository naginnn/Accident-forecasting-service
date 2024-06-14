import {useEffect, useState} from "react";
import {FetchBaseQueryError} from "@reduxjs/toolkit/dist/query/fetchBaseQuery";

import {useFetch} from "@src/shared/hooks/useFetch";

import {getFileName} from "@src/shared/lib/getFileName";
import {saveData} from "@src/shared/lib/saveData";

interface IUseDownloadReturnType {
    downloadFile: (url: string, headers: Record<string, string> | undefined) => void
    isLoading: boolean
    error: FetchBaseQueryError | undefined
    isSuccess: boolean | undefined
}

export const useDownloadFile = (): IUseDownloadReturnType => {
    const [fileName, setFileName] = useState<string>('')

    const onGetFileName = (response: Response) => {
        const fileName = getFileName(response) || 'default'
        setFileName(fileName)
    }

    const [makeFetch, {data, isLoading, error, isSuccess}] = useFetch<Blob>({
        responseCallback: onGetFileName
    })

    const downloadFile = (url: string, headers: Record<string, string> | undefined = {}) => {

        makeFetch({
            url,
            responseType: 'blob',
            headers,
        })
    }

    useEffect(() => {
        if (!isLoading && data) {
            saveData(data, fileName)
        }
    }, [isLoading, data])

    return {downloadFile, isLoading, error, isSuccess}
}