import {FC, useEffect} from "react";

import {Typography} from "@mui/material";

import {LoadingWrapper} from "@src/entities/loadingWrapper";
import {ErrorWrapper} from "@src/entities/errorWrapper";

import {useLazyGetConsumerQuery} from "../api/getConsumer";

interface SingleConsumerInfoProps {
    consumerId: number
}

export const SingleConsumerInfo: FC<SingleConsumerInfoProps> = ({consumerId}) => {
    const [fetchConsumer, {data, error, isLoading}] = useLazyGetConsumerQuery()

    useEffect(() => {
        fetchConsumer(consumerId)
    }, [consumerId])

    return <LoadingWrapper isLoading={isLoading} displayType='linear'>
        <ErrorWrapper
            fullSizeError={{
                error,
                blockContent: true
            }}
        >
        </ErrorWrapper>
    </LoadingWrapper>
};
