import {FC} from "react";

import {Modal, Box} from "@mui/material";

import {CenteredBox} from "@src/shared/ui/centeredBox";
import {PaperWrapper} from "@src/shared/ui/paperWrapper";

interface SettingModalProps {
    isOpen: boolean
    onClose: () => void
}

export const SettingModal: FC<SettingModalProps> = ({isOpen, onClose}) => {
    return (
        <Modal
            open={isOpen}
            onClose={onClose}
        >
            <Box>
                <CenteredBox
                    position='absolute'
                    sx={{position: 'absolute', width: '400px'}}
                >
                    <PaperWrapper sx={{mt: 0}}>
                        321
                    </PaperWrapper>
                </CenteredBox>
            </Box>
        </Modal>
    );
};
