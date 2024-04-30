export const handleErrorResponse = (response: any, meta: any) => {
    const requestId = meta?.requestId

    if (response.status === 'TIMEOUT_ERROR') {
        return {status: 503, data: {}}
    }
    return {...response, requestId};
}