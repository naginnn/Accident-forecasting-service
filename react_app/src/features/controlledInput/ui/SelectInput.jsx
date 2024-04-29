import {Controller} from "react-hook-form";

import {FormControl, Select} from "@mui/material";

import {LabelInput} from "./Labelnput";

export const SelectInput = ({name, control, children, labelName, errors = {}, sx = {}, ...props}) => {
    return (
        <FormControl size='small' fullWidth>
            <LabelInput
                errors={errors}
                name={name}
                label={labelName}
            />
            <Controller
                control={control}
                name={name}
                render={({field: {onChange, value}}) => (
                    <Select
                        onChange={onChange}
                        value={value}
                        error={!!errors[name]}
                        sx={{...sx}}
                        {...props}
                    >
                        {children}
                    </Select>
                )}
            >
            </Controller>
        </FormControl>
    )
}