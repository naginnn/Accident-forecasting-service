import {Checkbox, FormControlLabel, FormGroup} from "@mui/material";

interface IAuthPassShow {
    isVisiblePass: boolean;
    changePassShow: () => void;
}

export const AuthPassShow = ({isVisiblePass, changePassShow}: IAuthPassShow) => {
    return (
        <FormGroup sx={{mt: '24px'}}>
            <FormControlLabel
                control={
                    <Checkbox
                        disableRipple
                        checked={isVisiblePass}
                        onChange={changePassShow}
                    />
                }
                label='Показать пароль'
            />
        </FormGroup>
    )
}