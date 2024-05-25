import CircularProgress from '@mui/material/CircularProgress';
import {Box} from '@mui/material';

const CircleLoader = () => {
    return (
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
    )
}

export {CircleLoader};