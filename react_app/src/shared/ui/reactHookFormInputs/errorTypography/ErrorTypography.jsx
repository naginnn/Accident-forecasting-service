import {Typography} from "@mui/material";

export const ErrorTypography = ({children, sx, ...props}) => {
    return (
        <Typography mb='5px' color='red' sx={{...sx}} {...props}>
            {children}
        </Typography>
    )
}