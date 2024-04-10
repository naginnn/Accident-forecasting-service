import {Typography} from "@mui/material";
import {useTheme} from "@mui/material/styles";

interface InputText {
    errors?: {[x: string]: any},
    name?: string,
    label: string,
}
export const LabelInput = ({errors = {}, name = '', label}: InputText) => {
    const {palette} = useTheme()

    return (
        <Typography
            variant='subtitle1'
            sx={{
                color: errors[name]?.message ? palette.error.main : 'inherit',
                fontWeight: 500,
            }}
        >
            {label}
            {errors[name]?.message ? `: ${errors[name]?.message}` : ''}
        </Typography>
    )
}