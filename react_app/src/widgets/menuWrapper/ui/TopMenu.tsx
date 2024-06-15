import cls from './topMenu.module.scss'
import logo from '@src/shared/assets/logo.png'

import FileUploadIcon from '@mui/icons-material/FileUpload';

import {Box} from "@mui/material";

import {classNames} from '@src/shared/lib/classNames';
import {FocusedIcon} from '@src/shared/ui/focusedIcon';
import {useToggle} from '@src/shared/hooks/useToggle';
import {LoadingWrapper} from '@src/entities/loadingWrapper';
import {ErrorWrapper} from '@src/entities/errorWrapper';

import {UploadModal} from './UploadModal';
import {useUploadFile} from "../api/uploadFile";

interface ITopMenu {
    isMenuOpen: boolean
    menuIsVisible: boolean
}

export const TopMenu = ({menuIsVisible}: ITopMenu) => {
    const {on: openUploadModal, off: closeUploadModal, value: isOpenUploadModal} = useToggle()
    const {on: openSettingModal, off: closeSettingModal, value: isOpenSettubgModal} = useToggle()
    const {uploadData, isLoading, error} = useUploadFile()

    if (!menuIsVisible)
        return null

    return (
        <LoadingWrapper isLoading={isLoading} displayType='modalUnblock'>
            <ErrorWrapper
                snackBarErrors={{errors: [{error, message: 'Не удалось загрузить данные'}]}}
            >
                <div className={classNames(cls.topMenuWrapper)}>
                    <UploadModal
                        isOpen={isOpenUploadModal}
                        onClose={closeUploadModal}
                        fetchData={uploadData}
                    />
                    <Box sx={{height: '100%', width: '100%', px: '16px', display: 'flex', alignItems: 'center'}}>
                        <Box sx={{width: '100px', display: 'inline-block'}}>
                            <img src={logo} style={{width: '90%', maxHeight: '100%'}}/>
                        </Box>
                        <Box sx={{ml: 'auto', display: 'flex', gap: '8px', width: 'fit-content'}}>
                            <FocusedIcon onClick={openUploadModal}>
                                <FileUploadIcon/>
                            </FocusedIcon>
                        </Box>
                    </Box>
                </div>
            </ErrorWrapper>
        </LoadingWrapper>
    )
}