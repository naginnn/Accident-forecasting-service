import {SxProps, Theme } from "@mui/system";

import {Link as LinkMui} from "@mui/material";

interface ILinkedTypography {
    children?: React.ReactNode;
    sx?: SxProps<Theme>;
    [x: string]: any;
}

export const Link = ({sx, children, ...props}: ILinkedTypography) => {
    return (
        <LinkMui
            underline='hover'
            sx={{
                color: (theme) => theme.palette.primary.main,
                cursor: 'pointer',
                ...sx
            }}
            {...props}
        >
            {children}
        </LinkMui>
    );
}