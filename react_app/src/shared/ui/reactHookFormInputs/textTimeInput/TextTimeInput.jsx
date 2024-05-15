import {Controller} from "react-hook-form";

import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider";
import {AdapterDayjs} from '@mui/x-date-pickers/AdapterDayjs';
import {DemoContainer} from '@mui/x-date-pickers/internals/demo';
import {TimeField} from '@mui/x-date-pickers/TimeField';

// Добавить обработку error, если это возможно
export const TextTimeInput = ({name, control, label, sx, ...props}) => {
    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Controller
                control={control}
                name={name}
                render={({field: {value, onChange, ...field}}) => (
                    <DemoContainer components={['TimeField']}>
                        <TimeField
                            size='small'
                            label={label}
                            value={value}
                            onChange={onChange}
                            format="HH:mm"
                            sx={{...sx}}
                            {...field}
                            {...props}
                        />
                    </DemoContainer>
                )}/>
        </LocalizationProvider>
    )
};



