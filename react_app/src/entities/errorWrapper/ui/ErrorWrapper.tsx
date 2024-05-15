import {FC, ReactNode, useEffect, useMemo, useState} from "react"
import {useSnackbar} from 'notistack'

import {SerializedError} from "@reduxjs/toolkit";
import {FetchBaseQueryError} from "@reduxjs/toolkit/query/react";

import {isCustomFetchBaseQueryError} from "@src/shared/api/apiBase";
import {CustomFetchBaseQueryErrT} from "@src/shared/api/apiBase";

import {ErrorLayout} from "./ErrorLayout";

interface ISnackBarError {
    error: CustomFetchBaseQueryErrT | FetchBaseQueryError | SerializedError | boolean | undefined
    message: string
    blockContent?: boolean // Блокирует контент в случае возникновения конкретной ошибки
    onClose?: (...data: any[]) => void
    key?: string | number
}

interface IShowedSnackBar {
    [x: string]: boolean
}

interface IErrorWrapper {
    snackBarErrors?: {
        errors: ISnackBarError[]
        blockContent?: boolean // В случае возникновения хоть 1 ошибки в errors блокирует контент
    }
    fullSizeError?: {
        error: CustomFetchBaseQueryErrT | FetchBaseQueryError | SerializedError | boolean | undefined
        errorLayout?: ReactNode
        blockContent?: boolean
    }
    children: ReactNode
}

export const ErrorWrapper: FC<IErrorWrapper> = ({snackBarErrors, fullSizeError, children}) => {
    const [showedSnackBars, setShowedSnackBars] = useState<IShowedSnackBar | undefined>(() => {
        if (!snackBarErrors || !snackBarErrors.errors.length)
            return undefined

        const initObj: IShowedSnackBar = {}
        snackBarErrors.errors.forEach(({error, message, key}) => {
            if (!error) return

            if (key) {
                initObj[key] = false
            } else if (typeof error !== 'boolean' && isCustomFetchBaseQueryError(error)) {
                initObj[error.requestId] = false
            } else {
                initObj[message] = false
            }
        })

        return initObj
    })

    const {enqueueSnackbar} = useSnackbar()

    useEffect(() => {
        if (snackBarErrors && snackBarErrors.errors.length && showedSnackBars) {
            snackBarErrors.errors.forEach(({error, message, onClose, key}) => {
                if (!error || !message) return
                let keyActual: string | number = message // Уникальным ключем служит requestId (присваивается при каждом неудачном запрос), если есть.
                                                         // Либо message, либо key
                if (key) {
                    keyActual = key
                } else if (typeof error !== 'boolean' && isCustomFetchBaseQueryError(error)) {
                    keyActual = error.requestId
                }

                if (keyActual in showedSnackBars && !showedSnackBars[keyActual] || !(keyActual in showedSnackBars)) {
                    enqueueSnackbar(message, {variant: 'error', preventDuplicate: true, onClose, key: keyActual})

                    setShowedSnackBars((prev) => {
                        if (!prev) return prev

                        const copyPrev: IShowedSnackBar = {...prev}
                        copyPrev[keyActual] = true

                        return copyPrev
                    })
                }
            })
        }
    }, [snackBarErrors, enqueueSnackbar])

    const snackBarsBlockContent = useMemo(() => {
        let blockContent = false

        if (!snackBarErrors || !snackBarErrors.errors.length || !snackBarErrors.errors.some(err => err.error))
            return blockContent

        if ('blockContent' in snackBarErrors && typeof snackBarErrors.blockContent === 'boolean') {
            blockContent = snackBarErrors.blockContent
        } else {
            snackBarErrors.errors.forEach((err) => {
                if (err.error && 'blockContent' in err && err.blockContent) {
                    blockContent = err.blockContent
                }
            })
        }

        return blockContent
    }, [snackBarErrors])

    if (snackBarsBlockContent) {
        return null
    }

    if (fullSizeError && fullSizeError.error) {
        if (fullSizeError.blockContent) {
            if (fullSizeError.errorLayout) {
                return <>
                    {fullSizeError.errorLayout}
                </>
            }
            return <ErrorLayout error={fullSizeError.error}/>
        }

        if (fullSizeError.errorLayout) {
            return <>
                {fullSizeError.errorLayout}
                {children}
            </>
        }

        return <>
            <ErrorLayout
                error={fullSizeError.error}
            />
            {children}
        </>
    }

    return <>{children}</>
}