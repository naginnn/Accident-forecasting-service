import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {useForm} from "react-hook-form";
import {yupResolver} from "@hookform/resolvers/yup";
import {useTheme} from "@mui/material/styles";
import * as yup from "yup";

import {Grid, Button} from "@mui/material";

import {AuthHeader, AuthWrapper} from "@src/features/authentication";
import {AuthPassShow} from "@src/features/authentication";
import {getErrorMessage} from "@src/shared/lib/getErrorMessage";
import {TextInput} from "@src/shared/ui/reactHookFormInputs";
import {routerPaths} from "@src/shared/config/router";

import {useLazyLoginQuery} from '../api/makeLogin'

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

    const [
        loginFetch,
        {
            data: token,
            error: errorLogin,
            isFetching: isFetchingLogin,
            isSuccess: isSuccessLogin
        }
    ] = useLazyLoginQuery() // хук для логина

    const {control, resetField, setError, handleSubmit, formState: {errors}} = useForm({
        resolver: yupResolver(validationSchema),
        defaultValues: {
            login: '',
            password: '',
        }
    });

    // обработка ошибок логирования
    useEffect(() => {
        if (errorLogin) {
            resetField('password')
            if ('status' in errorLogin && errorLogin.status === 401) {
                setError('login', {message: 'Неправильный логин или пароль'})
            } else {
                setError('login', {message: getErrorMessage(errorLogin)})
            }
        } else if (isSuccessLogin && token) {
            localStorage.setItem('token', token)
        }

     }, [errorLogin, isSuccessLogin, isFetchingLogin, token, navigate, resetField, setError])

    const onSubmit = (data: FormData) => {
        loginFetch({
            login: data.login,
            password: data.password,
        })
    }

    return (
        <AuthWrapper>
            <AuthHeader
                topic='Вход'
                linkTopic='Зарегистрироваться'
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
                    disabled={isFetchingLogin}
                >
                    {isFetchingLogin ? 'Войти...' : 'Войти'}
                </Button>
            </form>
        </AuthWrapper>
    )
}