import {useCallback, useEffect, useState} from "react";
import {SessionStorageManager} from "../utils/sessionStorageManager";

// Принимает инициализирующие значения страницы и количество строк на странице, также Id таблицы
// Если переданы инициализирующие значение, то начальное состояние берется из них или из
// sessionStorage если передан tableId. onPaginationChange(page, rowsPerPage) - callback, который срабатывает при
// изменении количества элементов на страницы или страницы
// data нужна передавать только в том случае если передан callback onChangePagination
export const usePagination = ({pageInit, rowsPerPageInit, tableId, onChangePagination, data} = {}) => {
    const [rowsPerPage, setRowsPerPage] = useState(() => {
        if (typeof pageInit === 'number') return rowsPerPageInit
        if (tableId) {
            const rowsPerPage = SessionStorageManager.getPaginationValue(tableId).rowsPerPage
            if (typeof rowsPerPage === 'string') return +rowsPerPage
        }

        return 10
    })

    const [page, setPage] = useState(() => {
        if (typeof pageInit === 'number') return pageInit
        if (tableId) {
            const page = SessionStorageManager.getPaginationValue(tableId).page
            if (typeof page === 'string') return +page
        }

        return 0
    })

    // Хук который в случае изменении отображения таблицы (изменение кол-ва столбцов, кол-ва строк или данных)
    // Вызывает callback
    useEffect(() => {
        if (onChangePagination && typeof onChangePagination === 'function') {
            if (!data) {
                console.error('Data должна передаваться вместе с callback onChangePagination в хуке usePagination')
            }
            onChangePagination(getActualPage, rowsPerPage, getPageContent)
        }
    }, [rowsPerPage, page, data])

    const onChangePage = useCallback((event, newPage) => {
        if (tableId) {
            SessionStorageManager.setPaginationValue(tableId, newPage, rowsPerPage)
        }
        setPage(newPage);
    }, [rowsPerPage, tableId])

    const сhangeRowsPerPage = useCallback((event) => {
        if (tableId) {
            SessionStorageManager.setPaginationValue(tableId, 0, +event.target.value)
        }

        setPage( 0);
        setRowsPerPage(+event.target.value);
    }, [tableId])

    // Проверка есть ли контект на текущей странице, если контента нет
    // переключает на первую страницу, такое возможно когда данные динамически изменяются
    const getActualPage = (content) => {
        if (Math.trunc(content.length / rowsPerPage) < page) {
            onChangePage(undefined, 0)
            return 0
        }

        return page
    }

    const getPageContent = useCallback((content) => {
        const actualPage = getActualPage(content)

        return content.slice(actualPage * rowsPerPage, actualPage * rowsPerPage + rowsPerPage);
    }, [rowsPerPage, page])

    // Если данных стало меньше и такой страницы существовать не может, то
    // переключится на 1 страницу
    const getPage = useCallback((content) => {
        const actualPage = getActualPage(content)

        return actualPage
    }, [rowsPerPage, page])

    return {onChangePage, getPageContent, rowsPerPage, сhangeRowsPerPage, getPage};
}
