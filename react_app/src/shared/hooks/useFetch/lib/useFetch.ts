import {useEffect, useState} from "react";
import {FetchBaseQueryError} from "@reduxjs/toolkit/dist/query/fetchBaseQuery";

interface IMakeFetch {
    url: string
    method?: 'GET' | 'HEAD' | 'POST' | 'PUT' | 'DELETE' | 'CONNECT' | 'OPTIONS' | 'TRACE' | 'PATCH'
    responseType?: 'blob' | 'json'
    headers?: { [x: string]: string }
    extraHeaders?: { [x: string]: string }
    body?: BodyInit
}

interface IUseFetch {
    responseCallback?: (payload: any) => any
}

type UseFetchReturnType<T> = [
    (x: IMakeFetch) => void,
    {
        data: T | undefined,
        isLoading: boolean,
        error: FetchBaseQueryError | undefined,
        isSuccess: boolean | undefined
    }
]

export const useFetch = <T>({responseCallback}: IUseFetch): UseFetchReturnType<T> => {
    const [data, setData] = useState<T | undefined>()
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [error, setError] = useState<FetchBaseQueryError | undefined>()
    const [isSuccess, setIsSuccess] = useState<boolean| undefined>(undefined)

    const makeFetch = async (
        {
            url,
            method = 'GET',
            responseType = 'json',
            headers = {},
            extraHeaders = {},
            body
        }: IMakeFetch
    ) => {
        try {
            setIsLoading(true)
            const response = await fetch(url, {
                method: method,
                body: body,
                headers,
                ...extraHeaders,
            })

            if (!response.ok) {
                setError({status: response.status} as FetchBaseQueryError)
                setIsSuccess(false)
            } else {
                setIsSuccess(true)

                let payload;
                if (responseType === 'json') {
                    payload = await response.json()
                } else {
                    payload = await response.blob()
                }

                if (responseCallback && typeof responseCallback === 'function')
                    responseCallback(response)

                setData(payload)
            }
        } catch (e) {
            console.error(e)
            setError({status: 'FETCH_ERROR'} as FetchBaseQueryError)
            setIsSuccess(false)
        } finally {
            setIsLoading(false)
        }
    }

    useEffect(() => {
        if (error && error.status === 401) {
            localStorage.removeItem('token')
        }
    }, [error])

    return [makeFetch, {data, isLoading, error, isSuccess}]
}