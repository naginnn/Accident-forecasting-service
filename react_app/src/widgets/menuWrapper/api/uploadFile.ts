import {getRequestOptions, OBJ_URL} from "@src/shared/api/apiBase";
import {useFetch} from "@src/shared/hooks/useFetch";

export const useUploadFile = () => {
    const [fetch, {data, isLoading, error, isSuccess}] = useFetch<Blob>({})

    const uploadData = (file: FormData) => {
        const allHeaders = getRequestOptions()

        fetch({
            url: OBJ_URL + '/api/v1/train/upload',
            method: 'POST',
            body: file,
            headers: allHeaders.headers,
            extraHeaders: allHeaders.extraOptions,
            responseType: 'blob'
        })
    }

    return {uploadData, data, isLoading, error, isSuccess}
}