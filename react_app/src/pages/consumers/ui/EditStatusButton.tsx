import {FC} from "react";

import {green, red} from "@mui/material/colors";

import CloseIcon from '@mui/icons-material/Close';
import RemoveCircleOutlineOutlinedIcon from '@mui/icons-material/RemoveCircleOutlineOutlined';
import CheckIcon from '@mui/icons-material/Check';
import SettingsIcon from '@mui/icons-material/Settings';

import {ListItemIcon, ListItemText, MenuItem, MenuList} from "@mui/material";

import {IconButtonWithPopover} from "@src/entities/iconButtonWithPopover";

import {TransformConsumers} from "@src/pages/consumers/api/getConsumers";
import {manageConsumerStatus} from "@src/pages/consumers/utils/manageConsumerStatus";


interface EditStatusButtonProps {
    info: TransformConsumers
    updateStatus: React.Dispatch<React.SetStateAction<TransformConsumers[]>>
}

export const EditStatusButton: FC<EditStatusButtonProps> = ({info, updateStatus}) => {
    const editConsumerStatus = (keyName: keyof Pick<TransformConsumers, 'is_approved' | 'is_closed' | 'is_warning'>, val: boolean) => {
        updateStatus((consumers) => {
            return manageConsumerStatus(consumers, info.consumer_id, keyName, val)
        })
    }

    return (
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
            <MenuList autoFocusItem>
                <MenuItem
                    disabled={!info.is_warning}
                    onClick={() => {
                        editConsumerStatus('is_warning', false)
                    }}
                >
                    <ListItemIcon sx={{color: red[700]}}>
                        <RemoveCircleOutlineOutlinedIcon fontSize="small"/>
                    </ListItemIcon>
                    <ListItemText>Отклонить</ListItemText>
                </MenuItem>
                <MenuItem
                    disabled={info.is_approved || info.is_closed}
                    onClick={() => {
                        editConsumerStatus('is_closed', true)
                    }}
                >
                    <ListItemIcon sx={{color: red[700]}}>
                        <CloseIcon fontSize="small"/>
                    </ListItemIcon>
                    <ListItemText>Закрыть</ListItemText>
                </MenuItem>
                <MenuItem
                    disabled={info.is_approved || info.is_closed}
                    onClick={() => {
                        editConsumerStatus('is_approved', true)
                    }}
                >
                    <ListItemIcon sx={{color: green[700]}}>
                        <CheckIcon fontSize="small"/>
                    </ListItemIcon>
                    <ListItemText>Подтвердить</ListItemText>
                </MenuItem>
            </MenuList>
        </IconButtonWithPopover>
    );
};
