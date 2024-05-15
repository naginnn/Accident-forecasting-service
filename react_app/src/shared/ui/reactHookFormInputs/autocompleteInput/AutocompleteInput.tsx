import {Control, Controller} from "react-hook-form";
import {SxProps, Theme} from "@mui/material/styles";

import {Autocomplete, AutocompleteRenderOptionState, TextField} from "@mui/material"
import { HTMLAttributes, ReactNode } from "react";

interface IFormAutocompleteInput {
    name: string;
    control: Control<any>;
    label: string;
    options: any;
    noOptionsText?: string;
    isOptionEqualToValue?: (option: any, value: any) => boolean;
    getOptionDisabled?: (option: any) => boolean;
    getOptionLabel: (param: any) => string;
    renderOption?: (props: HTMLAttributes<HTMLLIElement>, option: any, state: AutocompleteRenderOptionState) => ReactNode,
    defaultValue?: any
    sx?: SxProps<Theme>;

    [x: string]: any
}

// getOptionLabel - необходимо обязательно, используется если не передаем разметку для опций
// noOptionsText - текст, если нет найденных параметров
// isOptionEqualToValue - необходимо указывать когда передаем объект в качестве параметра
// чтобы сравнивать выбранный результат
export const AutocompleteInput = (
    {
        name,
        control,
        label,
        options,
        getOptionLabel,
        renderOption,
        getOptionDisabled,
        isOptionEqualToValue,
        noOptionsText = 'Данный параметр отсутствует',
        sx,
        ...props
    }: IFormAutocompleteInput
) => {
    return (
        <Controller
            render={({field: {onChange, value}, formState: {errors}}) => {
                return <Autocomplete
                    sx={{...sx}}
                    size='small'
                    value={value}
                    options={options}
                    getOptionLabel={getOptionLabel}
                    isOptionEqualToValue={isOptionEqualToValue}
                    getOptionDisabled={getOptionDisabled}
                    renderOption={renderOption}
                    noOptionsText={noOptionsText}
                    renderInput={(params: any) => (
                        <TextField
                            {...params}

                            label={errors[name]?.message as string || label}
                            variant="outlined"
                        />
                    )}
                    onChange={(e: any, data: any) => onChange(data)}
                    {...props}
                />
            }}
            name={name}
            control={control}
        />
    )
}