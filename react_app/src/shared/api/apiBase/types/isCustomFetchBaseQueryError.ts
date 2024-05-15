import {SerializedError} from "@reduxjs/toolkit";
import {FetchBaseQueryError} from "@reduxjs/toolkit/dist/query/react";

import {CustomFetchBaseQueryErrT} from "./customFetchBaseQueryError";

export const isCustomFetchBaseQueryError = (error: CustomFetchBaseQueryErrT | SerializedError | FetchBaseQueryError): error is CustomFetchBaseQueryErrT => {
    return 'status' in error && 'requestId' in error
}