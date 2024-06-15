import {useState} from "react";
import copy from 'copy-to-clipboard';

import {Tooltip, useTheme, Box} from "@mui/material";

import {SxProps} from "@mui/material/styles";
import {Theme} from "@mui/system";

import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DoneIcon from '@mui/icons-material/Done';

interface ICopyClickBoardButton {
    text: string
    sx?: SxProps<Theme>

    [x: string]: any
}

/*
    Кнопка копирования текста

    text - текст копируется при нажатии на кнопку
    sx - стили для кнопки копирования
 */
export const CopyClickBoardBtn = ({text, sx = {}, ...props}: ICopyClickBoardButton) => {
    const {palette} = useTheme()

    // Флаг отвечающий за смену иконок копирования
    const [isCopied, setIsCopied] = useState<boolean>(false)

    const onCopy = (e: any) => {
        e.stopPropagation()

        // копирование текста в буффер обмена
        copy(text, {debug: true})
        setIsCopied(true)

        setTimeout(() => {
            setIsCopied(false)
        }, 2000)
    }

    return (
        <Tooltip
            open={isCopied}
            placement={'top'}
            componentsProps={{
                tooltip: {
                    sx: {backgroundColor: palette.success.main}
                }
            }}
            title='Скопировано'
        >
            <Box>
                <DoneIcon
                    color='success'
                    fontSize='small'
                    sx={{display: isCopied ? 'block' : 'none', ...sx}}
                />
                <ContentCopyIcon
                    onClick={onCopy}
                    onMouseDown={(e) => e.stopPropagation()}
                    fontSize='small'
                    sx={{
                        display: isCopied ? 'none' : 'block',
                        cursor: 'pointer',
                        ':hover': {color: 'initial'},
                        color: palette.grey[700],
                        ...sx
                    }}
                    {...props}
                />
            </Box>
        </Tooltip>
    )
}