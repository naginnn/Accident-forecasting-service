export const getRequestOptions = (headers?: Record<string, string>) => {
    return {
        headers,
        extraOptions: {
            credentials: "include",
        },
    }
}
