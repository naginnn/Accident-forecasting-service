import {useEffect, useRef, useState, MouseEvent, DragEvent} from 'react';
import {useSnackbar} from "notistack";

import InsertDriveFileOutlinedIcon from '@mui/icons-material/InsertDriveFileOutlined';

import {Box, Button, Grid, Typography} from "@mui/material"
import {SxProps, Theme} from "@mui/material/styles";

interface IFileDropAreaProps {
    sx?: SxProps<Theme>
    topic: string
    width: string
    height: string
    fileFormat?: string
    submitButtonTopic: string
    onSubmit: (file: FileList) => void
}

/*
    Компонент загрузки файла

    sx - стили для компонента обертки
    topic - заголовок модалки
    width - ширина модалки
    height - высота модалки
    fileFormat - формат принимаего файла, (например .txt)
    submitButtonTopic - имя кнопки сабмит
    onSubmit - колбек сабмита формы
*/
export const FileDropArea = ({
                                 sx,
                                 width,
                                 height,
                                 topic,
                                 fileFormat,
                                 submitButtonTopic,
                                 onSubmit
                             }: IFileDropAreaProps) => {
    const [files, setFiles] = useState<FileList | null>(null)
    const [dropZoneFocused, setDropZoneFocused] = useState<boolean>(false)
    const [isValidExt, setIsValidExt] = useState(true)
    const inputRef = useRef<HTMLInputElement>(null)

    const {enqueueSnackbar} = useSnackbar()

    // Проверяет загруженный файл на расширение
    // Расширение должно быть передано в формате '.jpg,.png'
    const checkValidExtension = (files: FileList, fileFormat: string) => {
        const isValidExtension = fileFormat.split(',')
            .some(format => {
                const trimmedFormat = format.trim()

                return files[0].name.includes(trimmedFormat)
            })

        return isValidExtension
    }

    // Очищает загруженный файл в том числе с input.files
    const clearFile = () => {
        inputRef!.current!.files = new DataTransfer().files
        setFiles(null)
    }

    // При изменении файла проверяется расширение
    // если расширение невалидно выводится ошибка
    // и очищается загруженный файл
    useEffect(() => {
        if (files && fileFormat) {
            if (!checkValidExtension(files, fileFormat)) {
                clearFile()
                setIsValidExt(false)
            }
        }
    }, [files])

    useEffect(() => {
        if (!isValidExt) {
            enqueueSnackbar(
                'Неверное формат файла',
                {
                    variant: 'error',
                    preventDuplicate: true,
                    onClose: () => setIsValidExt(false),
                    key: 'Неверное формат файла'
                }
            )
        }
    }, [isValidExt, setIsValidExt])

    // Сохранение файла
    // Если был загружен до этого файл, а новый прикрепленный невалидный
    // тогда новый сбрасываем, старый оставляем. Иначе загружаем новый файл
    const handleSaveFile = (newFiles: FileList | null) => {
        setIsValidExt(true)
        setDropZoneFocused(false)
        if (!newFiles || !newFiles.length) {
            return
        } else if (files && fileFormat && !checkValidExtension(newFiles, fileFormat)) {
            setIsValidExt(false)
            return
        }

        setFiles(newFiles)
    }

    // Обработчик события когда перетаскиваемый объект над зоной дропа
    const handleDragOver = (e: DragEvent) => {
        if (!dropZoneFocused)
            setDropZoneFocused(true)

        e.preventDefault()
    }

    // Обработчик события когда перетаскиваемый объект покинул зону дропа
    const handleDragLeave = (e: DragEvent) => {
        if (dropZoneFocused)
            setDropZoneFocused(false)

        e.preventDefault()
    }

    // Обработчик события когда перетаскиваемый объект был сброшен
    const handleDrop = (e: DragEvent) => {
        e.preventDefault()
        handleSaveFile(e.dataTransfer.files)
    }

    // функция отправки файла
    const handleSumbit = (e: MouseEvent) => {
        e.stopPropagation()
        onSubmit(files!)
        clearFile()
        setIsValidExt(true)
    }

    return (
        <Box
            onMouseEnter={() => setDropZoneFocused(true)}
            onMouseLeave={() => setDropZoneFocused(false)}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => inputRef!.current!.click()}
            sx={{
                ...sx,
                borderRadius: '10px',
                bgcolor: dropZoneFocused ? 'rgba(255, 255, 255, .8)' : '#ffffff',
                border: '2px dashed #ffffff',
                backgroundClip: 'padding-box',
                color: 'black',
                cursor: 'pointer',
                transition: 'all .3s ease-in-out',
                width,
                height
            }}
        >
            <Box sx={{display: 'none', width: '100%', height: '100%'}}>
                <input
                    type='file'
                    accept={fileFormat}
                    onChange={(e) => handleSaveFile(e.target.files)}
                    hidden
                    ref={inputRef}
                />
            </Box>
            <Grid
                container
                alignItems='center'
                justifyContent='center'
                flexDirection='column'
                sx={{width: '100%', height: '100%'}}
            >
                <Grid item>
                    <InsertDriveFileOutlinedIcon
                        color='success'
                        fontSize='large'
                    />
                </Grid>
                <Grid item>
                    <Typography>
                        {topic}
                    </Typography>
                </Grid>
                {
                    files &&
                    <>
                        <Grid item>
                            <Typography sx={{fontWeight: '500'}}>
                                {files[0]?.name}
                            </Typography>
                        </Grid>
                        <Grid item sx={{mt: '10px'}}>
                            <Button
                                onMouseEnter={(e) => {
                                    e.stopPropagation();
                                    setDropZoneFocused(false)
                                }}
                                onMouseLeave={() => setDropZoneFocused(true)}
                                color='success'
                                onClick={handleSumbit}
                                variant='main-outlined'
                            >
                                {submitButtonTopic}
                            </Button>
                        </Grid>
                    </>
                }
            </Grid>
        </Box>
    )
}
