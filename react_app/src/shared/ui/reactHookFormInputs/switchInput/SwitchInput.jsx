import {Switch} from "@mui/material";
import {Controller} from "react-hook-form";

export const SwitchInput = ({name, control, sx = {}, ...props}) => {
    return (
        <Controller
            name={name}
            control={control}
            render={({field}) => {
                return (
                    (
                        <Switch
                            {...props}
                            onChange={(e) => field.onChange(e.target.checked)}
                            checked={field.value}/>
                    )
                )
            }}
        />
    )
}