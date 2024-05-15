import TextField from "@mui/material/TextField";
import {Controller} from "react-hook-form";

export const TextInput = ({name = '', control, label = '', sx = {}, ...props}) => {
    return (
        <Controller
            name={name}
            control={control}
            render={({field: {ref, value, ...field}, formState: {errors}}) => (
                    <TextField
                        {...props}
                        inputRef={ref}
                        value={value}
                        label={errors[name]?.message || label}
                        sx={{...sx}}
                        {...field}
                        error={!!errors[name]}
                        fullWidth
                        size='small'
                        variant="outlined"
                    />
            )}
            />
    )
};

