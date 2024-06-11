import {FC} from "react";

import {Theme} from "@mui/system";
import {Icon, IconProps, useTheme} from "@mui/material";
import {SxProps} from "@mui/material/styles";

interface IFocusedIcon extends IconProps {
    disabledFocus?: boolean
    children: any
    sxColor?: string
    sxColorFocus?: string
    sx?: SxProps<Theme>

    [x: string]: any
}


/*
    Компонент подсвечиваемой иконки, используется в меню

    disabledFocus - TODO если true, то меняются стили, но кнопка не становится реально disable, переделать
    children - иконка
    sxColor - цвет иконки
    sxColorFocus - цвет при фокусировки иконки
    sx - др стили
*/
export const FocusedIcon: FC<IFocusedIcon> = ({disabledFocus = false, sxColor, sxColorFocus ,sx, children, ...props}) => {
    const {palette} = useTheme()

    return (
        <Icon
            sx={{
                width: '30px',
                height: '30px',
                borderRadius: '5px',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                color: sxColor || palette.primary.main,
                'img': {
                    width: '25px',
                    filter: 'invert(34%) sepia(94%) saturate(820%) hue-rotate(177deg) brightness(98%) contrast(93%)'
                },
                '&:hover': {
                    cursor: 'pointer',
                    color: disabledFocus ? 'inherit' : sxColorFocus || palette.primary.light,
                    backgroundColor: disabledFocus ? 'inherit' : palette.grey[100],
                    'img': {
                        filter: 'invert(68%) sepia(79%) saturate(4123%) hue-rotate(185deg) brightness(103%) contrast(92%) !important'
                    }
                },
                ...sx
            }}
            {...props}
        >
            {children}
        </Icon>
    )
}
