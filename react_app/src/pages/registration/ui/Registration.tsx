// import * as yup from "yup";
// import {useForm} from "react-hook-form";
// import {useEffect, useState} from "react";
// import {useTheme} from "@mui/material/styles";
// import {useNavigate} from "react-router-dom";
// import {yupResolver} from "@hookform/resolvers/yup";
//
// import {Grid, MenuItem} from "@mui/material";
//
// import {AuthHeader, AuthWrapper, useRegistrationMutation} from "../../../features/authentication";
// import {AuthPassShow} from "../../../features/authentication";
// import {TextInput} from "../../../features/controlledInput/ui/TextInput";
// import {SubmitButton} from "../../../shared/button";
// import {SelectInput} from "../../../features/controlledInput";
// import {rolesOpt} from "../const/rolesOpt";
// import {getErrorMessage} from "../../../shared/error";
//
// const validationSchema = yup.object(
//     {
//         login: yup.string().required('Обязательное поле'),
//         password: yup.string().required('Обязательное поле'),
//         confirmPass: yup.string().required('Обязательное поле'),
//         roles: yup.string().required('Обязательное поле')
//     }
// )
//
// type FormData = yup.InferType<typeof validationSchema>
//
// // Страница регистрации пользователя
export const Registration = () => {
//     const navigate = useNavigate()
//     const {palette} = useTheme()
//     const [isVisiblePass, setIsVisiblePass] = useState<boolean>(false) // стейт для отображения/ скрытя пароля
//
//     const [registrationFetch, {error: errorRegistration, isLoading, isSuccess}] = useRegistrationMutation() // хук регистрации
//
//     const {control, resetField, setError, handleSubmit, formState: {errors}} = useForm({
//         resolver: yupResolver(validationSchema),
//         defaultValues: {
//             login: '',
//             password: '',
//             confirmPass: '',
//             roles: 'user'
//         }
//     });
//
//     useEffect(() => {
//         // блок обработки ошибок
//         if (errorRegistration) {
//             // @ts-ignore
//             if (errorRegistration.status === 401) {
//                 setError('login', {type: 'custom', message: 'Данный пользователь уже существует'})
//             } else {
//                 setError('login', {type: 'custom', message: getErrorMessage(errorRegistration)})
//             }
//             resetField('confirmPass')
//             resetField('password')
//         } else if (isSuccess) {
//             navigate('/login')
//         }
//     }, [errorRegistration, isSuccess, navigate, resetField, setError])
//
//     const onSubmit = (data: FormData) => {
//         const {confirmPass, password, login, roles} = data;
//         if (confirmPass !== password) {
//             setError('password', {type: 'custom', message: 'пароли должны совпадать'})
//             setError('confirmPass', {type: 'custom', message: ''})
//             return
//         }
//
//         registrationFetch({
//             username: login,
//             roles: roles === 'user' ? roles : `${roles},user`,
//             password
//         })
//     }
    return <div>132</div>
//     return (
//         <AuthWrapper>
//             <AuthHeader
//                 topic='Регистрация'
//                 linkTopic='Войти'
//                 href='/login'
//             />
//             <form onSubmit={handleSubmit(onSubmit)}>
//                 <Grid container direction='column' alignItems='center' rowSpacing={3}>
//                     <Grid item width='100%'>
//                         <TextInput
//                             errors={errors}
//                             control={control}
//                             label='Логин'
//                             type='login'
//                             name='login'
//                         />
//                     </Grid>
//                     <Grid item width='100%'>
//                         <SelectInput
//                             errors={errors}
//                             control={control}
//                             name='roles'
//                             id='user_role'
//                             labelName='Выберите роль'
//                         >
//                             {
//                                 rolesOpt.map((opt) => {
//                                     return (
//                                         <MenuItem
//                                             key={opt.name}
//                                             value={opt.value}
//                                         >
//                                             {opt.name}
//                                         </MenuItem>
//                                     )
//                                 })
//                             }
//                         </SelectInput>
//                     </Grid>
//                     <Grid item width='100%'>
//                         <TextInput
//                             errors={errors}
//                             control={control}
//                             label='Пароль'
//                             type={isVisiblePass ? 'text' : 'password'}
//                             name='password'
//                         />
//                     </Grid>
//                     <Grid item width='100%'>
//                         <TextInput
//                             errors={errors}
//                             control={control}
//                             label='Повторите пароль'
//                             type={isVisiblePass ? 'text' : 'password'}
//                             name='confirmPass'
//                         />
//                     </Grid>
//                 </Grid>
//                 <AuthPassShow
//                     isVisiblePass={isVisiblePass}
//                     changePassShow={() => setIsVisiblePass(prev => !prev)}
//                 />
//                 <SubmitButton disabled={isLoading} bgcolor={palette.primary.dark}>
//                     {isLoading ? 'Регистрация...' : 'Зарегистрироваться'}
//                 </SubmitButton>
//             </form>
//
//         </AuthWrapper>
//     )
}