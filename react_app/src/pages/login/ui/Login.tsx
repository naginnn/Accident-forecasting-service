import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {useForm} from "react-hook-form";
import {yupResolver} from "@hookform/resolvers/yup";
import {useTheme} from "@mui/material/styles";
import * as yup from "yup";

import {Grid, Button} from "@mui/material";

import {AuthHeader, AuthWrapper} from "../../../features/authentication";
import {AuthPassShow} from "../../../features/authentication";
import {getErrorMessage} from "../../../shared/lib/getErrorMessage";
import { TextInput } from "../../../features/controlledInput";
import { routerPaths } from "@src/shared/config/router";

const validationSchema = yup.object(
    {
        login: yup.string().required('Обязательное поле'),
        password: yup.string().required('Обязательное поле')
    }
)

type FormData = yup.InferType<typeof validationSchema>

// Cтраница логина
export const Login = () => {
    const navigate = useNavigate()

    const {palette} = useTheme()
    const [isVisiblePass, setIsVisiblePass] = useState<boolean>(false)

    // const [loginFetch, {data: token, error: errorLogin, isLoading, isSuccess}] = useLoginMutation() // хук для логина

    const {control, resetField, setError, handleSubmit, formState: {errors}} = useForm({
        resolver: yupResolver(validationSchema),
        defaultValues: {
            login: '',
            password: '',
        }
    });

    // обработка ошибок логирования
    // useEffect(() => {
    //     if (errorLogin) {
    //         resetField('password')
    //         // @ts-ignore
    //         if (errorLogin.status === 401) {
    //             setError('login', {message: 'Неправильный логин или пароль'})
    //         } else {
    //             setError('login', {message: getErrorMessage(errorLogin)})
    //         }
    //     } else if (isSuccess) {
    //         localStorage.setItem('token', token)
    //         navigate('/recommendation')
    //     }
    //
    //  }, [errorLogin, isSuccess, token, navigate, resetField, setError])

    const onSubmit = (data: FormData) => {
        const data64 = btoa(`${data.login}:${data.password}`)

        // loginFetch(data64)
    }

    return (
        <AuthWrapper>
            <AuthHeader
                topic='Вход'
                linkTopic='зарегистрироваться'
                href={routerPaths.registration}
            />
            <form onSubmit={handleSubmit(onSubmit)}>
                <Grid container direction='column' alignItems='center' rowSpacing={3}>
                    <Grid item width='100%'>
                        <TextInput
                            errors={errors}
                            control={control}
                            label='Логин'
                            name='login'
                        />
                    </Grid>
                    <Grid item width='100%'>
                        <TextInput
                            errors={errors}
                            control={control}
                            label='Пароль'
                            type={isVisiblePass ? 'text' : 'password'}
                            name='password'
                        />
                    </Grid>
                </Grid>
                <AuthPassShow
                    isVisiblePass={isVisiblePass}
                    changePassShow={() => setIsVisiblePass(prev => !prev)}
                />
                <Button
                    fullWidth
                    type="submit"
                    variant="contained"
                    sx={{mt: '24px', bgcolor: palette.primary.dark}}
                    // disabled={isLoading}
                >
                    Войти
                    {/*{isLoading ? 'Войти...' : 'Войти'}*/}
                </Button>
            </form>
        </AuthWrapper>
    )
}