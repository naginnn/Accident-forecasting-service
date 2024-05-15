import {Controller} from "react-hook-form";

import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider";
import {AdapterDayjs} from '@mui/x-date-pickers/AdapterDayjs';
import {DemoContainer} from '@mui/x-date-pickers/internals/demo';
import { DateField } from '@mui/x-date-pickers/DateField';

export const DataInput = ({name, control, label, sx, error, ...props}) => {
    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Controller
                control={control}
                name={name}
                render={({field: {value, onChange, ...field}}) => (
                    <DemoContainer components={['DatePicker']}>
                        <DateField
                            size='small'
                            format="DD-MM-YYYY"
                            label={label}
                            value={value}
                            onChange={onChange}
                            sx={{...sx}}
                            {...field}
                            {...props}
                        />
                    </DemoContainer>
                )}/>
        </LocalizationProvider>
    );
}
