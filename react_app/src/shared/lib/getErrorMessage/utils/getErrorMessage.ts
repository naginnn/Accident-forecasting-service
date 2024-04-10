export const getErrorMessage = (error: any) => {
    if (error?.name) {
        return error.name
    }
    if (!error || !error.status)
        return 'Что-то пошло не так'

    switch (error.status) {
        case 400:
            return 'Неправильная форма запроса'
        case 401:
            return 'Вы не авторизованы'
        case 403:
            return 'Нет доступа к данному ресурсу'
        case 404:
            return 'Не найдено'
        case 304:
            return 'Нет необходимости повторно передавать запрошенные ресурсы'
        case 500:
            return 'Внутренняя ошибка сервера, попробуйте позже'
        case 503:
            return 'Сервер не отвечает, попробуйте позже'
        default:
            return 'Что-то пошло не так'
    }
}