import {Box, Modal} from "@mui/material";

import {CenteredBox} from "@src/shared/ui/centeredBox";
import {FileDropArea} from "@src/entities/fileDropArea";

interface IUploadModal {
    isOpen: boolean
    onClose: () => void
    fetchData: (file: FormData) => void
}

/*
    Компонент массового поиска, загружается excel и возвращается обогащенный excel

    isOpen - стейт модалки
    onClose - обработчик закрытия модалки
    fetchData - функции отправляющая excel на бэк
*/
export const UploadModal = ({isOpen, onClose, fetchData}: IUploadModal) => {
    // фун-я отправки файла
    const onUploadFile = (files: FileList) => {
        const file = files[0];
        const formData = new FormData();
        formData.append('file', file, file.name)
        fetchData(formData)
    }

    return (
        <Modal
            open={isOpen}
            onClose={onClose}
        >
            <Box>
                <CenteredBox
                    position='absolute'
                    sx={{position: 'absolute', width: '400px'}}
                >
                    <FileDropArea
                        width='100%'
                        height='200px'
                        topic='Загрузите файл'
                        fileFormat=".zip"
                        submitButtonTopic='Отправить'
                        onSubmit={onUploadFile}
                    />
                </CenteredBox>
            </Box>
        </Modal>
    )
}