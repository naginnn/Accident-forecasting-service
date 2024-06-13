import {FC, useEffect} from "react";

import {green, red} from "@mui/material/colors";

import CloseIcon from '@mui/icons-material/Close';
import RemoveCircleOutlineOutlinedIcon from '@mui/icons-material/RemoveCircleOutlineOutlined';
import CheckIcon from '@mui/icons-material/Check';
import SettingsIcon from '@mui/icons-material/Settings';

import {ListItemIcon, ListItemText, MenuItem, MenuList} from "@mui/material";

import {IconButtonWithPopover} from "@src/entities/iconButtonWithPopover";

import {TransformConsumers} from "@src/pages/consumers/api/getConsumers";
import {manageConsumerStatus} from "@src/pages/consumers/utils/manageConsumerStatus";
import {LoadingWrapper} from "@src/entities/loadingWrapper";
import { ErrorWrapper } from "@src/entities/errorWrapper";

import {useApproveIncidentMutation} from "../api/approveIncident";
import {useCancelIncidentMutation} from "../api/cancelIncident";
import {useCloseIncidentMutation} from "../api/closeIncident";

interface EditStatusButtonProps {
    info: TransformConsumers
    updateStatus: React.Dispatch<React.SetStateAction<TransformConsumers[]>>
}

export const EditStatusButton: FC<EditStatusButtonProps> = ({info, updateStatus}) => {
    const [approveInc, {error: errorApprove, isLoading: isLoadingApprove, isSuccess: isSuccessApprove}] = useApproveIncidentMutation()
    const [cancelInc, {error: errorCancel, isLoading: isLoadingCancel, isSuccess: isSuccessCancel}] = useCancelIncidentMutation()
    const [closeInc, {error: errorClose, isLoading: isLoadingClose, isSuccess: isSuccessClose}] = useCloseIncidentMutation()

    const editConsumerStatus = (keyName: keyof Pick<TransformConsumers, 'is_approved' | 'is_closed' | 'is_warning'>, val: boolean) => {
        updateStatus((consumers) => {
            return manageConsumerStatus(consumers, info.consumer_id, keyName, val)
        })
    }

    useEffect(() => {
        if (errorClose) {
            editConsumerStatus('is_closed', false)
        } else if (isSuccessClose) {
            editConsumerStatus('is_closed', true)
        }
    }, [errorClose, isSuccessClose])

    useEffect(() => {
        if (errorCancel) {
            editConsumerStatus('is_warning', true)
        } else if (isSuccessCancel) {
            editConsumerStatus('is_warning', false)
        }
    }, [errorCancel, isSuccessCancel])

    useEffect(() => {
        if (errorApprove) {
            editConsumerStatus('is_approved', false)
        } else if (isSuccessApprove) {
            editConsumerStatus('is_approved', true)
        }
    }, [errorApprove, isSuccessApprove])


    return (
        <LoadingWrapper
            isLoading={isLoadingApprove || isLoadingCancel || isLoadingClose}
            displayType='modalUnblock'
        >
            <ErrorWrapper
                snackBarErrors={{
                    errors: [
                        {
                            error: errorApprove,
                            message: 'Не удалось подтвердить инциндент'
                        },
                        {
                            error: errorCancel,
                            message: 'Не удалось отклонить инциндент'
                        },
                        {
                            error: errorClose,
                            message: 'Не удалось закрыть инциндент'
                        }
                    ],
                }}
            >
                <IconButtonWithPopover
                    buttonIcon={<SettingsIcon/>}
                    anchorOrigin={{
                        vertical: 'center',
                        horizontal: 'left',
                    }}
                    transformOrigin={{
                        vertical: 'center',
                        horizontal: 'right',
                    }}
                >
                    <MenuList autoFocusItem onClick={(e) => e.stopPropagation()}>
                        <MenuItem
                            disabled={!info.is_warning}
                            onClick={(e) => {
                                e.stopPropagation()
                                cancelInc(info.consumer_id)
                            }}
                        >
                            <ListItemIcon sx={{color: red[700]}}>
                                <RemoveCircleOutlineOutlinedIcon fontSize="small"/>
                            </ListItemIcon>
                            <ListItemText>Отклонить</ListItemText>
                        </MenuItem>
                        <MenuItem
                            disabled={!info.is_approved || info.is_closed}
                            onClick={(e) => {
                                e.stopPropagation()
                                closeInc(info.consumer_id)
                            }}
                        >
                            <ListItemIcon sx={{color: red[700]}}>
                                <CloseIcon fontSize="small"/>
                            </ListItemIcon>
                            <ListItemText>Закрыть</ListItemText>
                        </MenuItem>
                        <MenuItem
                            disabled={info.is_approved || info.is_closed}
                            onClick={(e) => {
                                e.stopPropagation()
                                approveInc(info.consumer_id)
                            }}
                        >
                            <ListItemIcon sx={{color: green[700]}}>
                                <CheckIcon fontSize="small"/>
                            </ListItemIcon>
                            <ListItemText>Подтвердить</ListItemText>
                        </MenuItem>
                    </MenuList>
                </IconButtonWithPopover>
            </ErrorWrapper>
        </LoadingWrapper>
    );
};
