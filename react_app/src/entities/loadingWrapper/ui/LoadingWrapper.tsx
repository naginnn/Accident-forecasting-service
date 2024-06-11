import {ReactNode} from "react";

import {CircleLoader, ModalLoader} from "@src/shared/ui/loader"

import {exhaustiveCheck} from "@src/shared/lib/exhaustiveCheck";
import {Box, LinearProgress} from "@mui/material";

interface ILoadingWrapperProps {
    isLoading: boolean
    displayType: 'normal' | 'modal' | 'hidden' | 'skeleton' | 'linear' | 'modalUnblock'
    skeletonLayout?: JSX.Element | React.ReactElement<any, any>
    children: ReactNode
}

export const LoadingWrapper = (
    {
        isLoading,
        displayType,
        skeletonLayout,
        children,
    }: ILoadingWrapperProps): null | JSX.Element | React.ReactElement<any, any> => {

    if (isLoading) {
        switch (displayType) {
            case "normal":
                return <CircleLoader/>
            case "modal":
                return <ModalLoader/>
            case "modalUnblock":
                return <>
                    <ModalLoader/>
                    {children}
                </>
            case "skeleton":
                return skeletonLayout ? skeletonLayout : null
            case "linear":
                return <Box sx={{width: '100%', my: '16px'}}>
                    <LinearProgress/>
                </Box>
            case "hidden":
                return null
            default: {
                exhaustiveCheck(displayType, `Данный тип отображения загрузки отсутствует - ${displayType}`)
                return null
            }
        }
    }

    return <>
        {children}
    </>
}