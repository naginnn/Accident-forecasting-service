import {cloneElement, JSXElementConstructor, ReactElement, useState} from "react";

import {SxProps} from "@mui/material/styles";

import {useToggle} from "src/shared/hooks/useToggle";

import {IconButton, Popover, Theme} from "@mui/material";

interface IButtonWithPopoverProps {
    buttonIcon: ReactElement<any, string | JSXElementConstructor<any>>
    children: React.ReactNode
    buttonSx?: SxProps<Theme>

    [x: string]: any
}

export const IconButtonWithPopover = ({buttonIcon, children, buttonSx = {}, ...props}: IButtonWithPopoverProps) => {
    const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null) // элемент к которому прикрепляется модалка
    const {value: isModalOpen, off: onCloseModal, on: onOpenModal} = useToggle(false)

    const onCloseMenu = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        e.stopPropagation()
        setAnchorEl(null)
        onCloseModal()
    }

    const onOpenMenu = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        e.stopPropagation()
        setAnchorEl(e.currentTarget)
        onOpenModal()
    }

    return (
        <>
            <IconButton size='small' onClick={onOpenMenu}>
                {
                    cloneElement(buttonIcon, {
                        sx: {color: (theme: Theme) => isModalOpen ? theme.palette.primary.main : '#616161', ...buttonSx}
                    })
                }
            </IconButton>
            <Popover
                open={isModalOpen}
                anchorEl={anchorEl}
                onClose={onCloseMenu}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                }}
                PaperProps={{
                    style: {
                        minHeight: '40px',
                        maxHeight: '350px',
                        minWidth: '150px',
                        width: 'max-content',
                    },
                }}
                {...props}
            >
                {children}
            </Popover>
        </>
    )
}