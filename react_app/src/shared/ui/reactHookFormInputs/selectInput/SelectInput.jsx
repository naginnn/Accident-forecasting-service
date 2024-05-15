import {Controller} from "react-hook-form";
import {FormControl, InputLabel} from "@mui/material";
import Select from "@mui/material/Select";

export const SelectInput = ({name, control, children, id, labelName, errors = {}, sx = {}, ...props}) => {
    return (
        <FormControl size='small' fullWidth>
            <InputLabel id={id}>{errors[name]?.message || labelName}</InputLabel>
            <Controller
                control={control}
                name={name}
                render={({field: {onChange, value}}) => (
                    <Select
                        labelId={id}
                        label={errors[name]?.message || labelName}
                        id={id}
                        onChange={onChange}
                        value={value}
                        sx={{...sx}}
                        {...props}
                        error={!!errors[name]}
                    >
                        {children}
                    </Select>
                )}
            />
        </FormControl>
    )
}
