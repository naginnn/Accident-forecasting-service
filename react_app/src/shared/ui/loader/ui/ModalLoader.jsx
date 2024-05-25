import Modal from "@mui/material/Modal";
import CircularProgress from "@mui/material/CircularProgress";
import {Box} from "@mui/material";


const ModalLoader = ({sx={}}) => {
    return (
        <Modal open sx={{zIndex: '99999', height: '100%', ...sx}}>
            <Box
                sx={{
                    position: 'relative',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    display: 'flex',
                    justifyContent: 'center'
                }}
            >
                <CircularProgress color='inherit'/>
            </Box>
        </Modal>
    );
}

export {ModalLoader};