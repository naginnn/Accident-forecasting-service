import {Controller} from "react-hook-form";
import TextField from "@mui/material/TextField";

export const TextPlaceholder = ({name, minRows = 1, control, label, errors = {}, sx = {}, ...props}) => {
    return (
        <Controller
            control={control}
            render={({field: {ref, ...field}}) => (
                <TextField
                    size='small'
                    inputRef={ref}
                    minRows={minRows}
                    variant="outlined"
                    error={!!errors[name]}
                    multiline
                    label={errors[name]?.message || label}
                    sx={{...sx}}
                    {...props}
                    {...field}/>
            )}
            name={name}/>
    )
}
