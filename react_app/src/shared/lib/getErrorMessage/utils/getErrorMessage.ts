type Error = {
    [x: string]: any;
}

export const getErrorMessage = (error: Error) => {
    if (!error || !error.status)
        return 'Что-то пошло не так'

    switch (error.status) {
        case 304:
            return 'Нет необходимости повторно передавать запрошенные ресурсы'
        case 400:
            return 'Неправильная форма запроса';
        case 401:
            return 'Вы не авторизованы, авторизуйтесь';
        case 403:
            return 'Нет доступа к данному ресурсу';
        case 404:
            return 'Не найдено'
        case 405:
            return 'Метод не разрешен'
        case 407:
            return 'Вы не авторизованы, авторизуйтесь'
        case 408:
            return 'Request Timeout'
        case 409:
            return 'Конфликт с текущим состоянием сервера'
        case 410:
            return 'Запрашиваемый контент удалён с сервера'
        case 411:
            return 'Заголовок Content-Length отсутствует'
        case 412:
            return 'Неверный заголовки'
        case 413:
            return 'Превышен лимит запроса'
        case 414:
            return 'Слишком длинный URL'
        case 415:
            return 'Неверный медиаформат'
        case 416:
            return 'Неверный Range'
        case 417:
            return 'Неверный Expect'
        case 500:
            return 'Внутренняя ошибка сервера, попробуйте позже'
        case 502:
            return 'Bad Gateway'
        case 503:
            return 'Ceрвер не отвечает, попробуйте позже'
        case 504:
            return 'Gateway Timeout'
        case 505:
            return 'HTTP-версия не поддерживается'
        default:
            return 'Что-то пошло не так'
    }
}

