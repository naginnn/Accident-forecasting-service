import {useCallback, useEffect} from "react";
import PropTypes from 'prop-types'

import Box from "@mui/material/Box";

import {SearchInput} from "@src/shared/ui/searchInput";

import {ManageColumnButton} from "./ManageColumnButton";
import {SessionStorageManager} from "../../utils/sessionStorageManager";
import {BANNER_CHILD_NAME} from "../../const/CellNames";

// findIntersection - функция для кастомного поиска значений (принимает дату и поисковое значение), должно быть обернутов в callBack
// tooltipTitle - подсказка
// tooltipPlacement - расположение подсказки
// withSearch - boolean для отображения поиска
// setWithSearchOuter - принимается из tableFilter, исходя из этого значения данные по поиску либо фильтруются либо нет
// setCustomIntersection - для передачи кастомного поиска по данных в компонент TableFilterSkeleton
// findIntersection - кастомный поиск
// filterValue - значение принимаемое из таблицы для контролируемого инпута
// onSearchInput - функция для контролируемого инпута
// onChangeVisibleColumn - callBack, который передает наверх объект с id колонок и информаций об их видимости
export const Banner = (
    {
        withSearch = false,
        withManageColumn = false,
        setWithSearchOuter,
        setWithManageColumnOuter,
        visibleColumn,
        defaultVisibleColumn, // В качестве значенией передаем массив id
        setVisibleColumn,
        tooltipTitle,
        tooltipPlacement,
        filterValue,
        setCustomIntersection,
        onSearchInput,
        findIntersection,
        dataCellProps,
        tableId,
        children
    }) => {
    const onToggleColumn = useCallback((id) => {
        setVisibleColumn((prev) => {
            const selectedColumnCopy = JSON.parse(JSON.stringify(prev))
            selectedColumnCopy[id] = !selectedColumnCopy[id]

            SessionStorageManager.setVisibleColumnsValue(tableId, selectedColumnCopy)
            return selectedColumnCopy
        })
    }, [])

    const onToggleAllColumn = useCallback((val) => {
        setVisibleColumn((prev) => {
            const selectedColumnCopy = JSON.parse(JSON.stringify(prev))
            Object.keys(selectedColumnCopy).forEach(id => {
                selectedColumnCopy[id] = val
            })

            SessionStorageManager.setVisibleColumnsValue(tableId, selectedColumnCopy)

            return selectedColumnCopy
        })
    }, [])

    useEffect(() => {
        if (findIntersection) setCustomIntersection(() => findIntersection)

        if (withSearch) setWithSearchOuter(true)

        if (withManageColumn) setWithManageColumnOuter(true)

        if (withManageColumn && defaultVisibleColumn && tableId && !SessionStorageManager.getUnvisibleColumnsVal(tableId).length) {
            setVisibleColumn(prev => {
                const selectedColumnCopy = JSON.parse(JSON.stringify(prev))

                Object.keys(selectedColumnCopy).forEach(id => {
                    selectedColumnCopy[id] = false
                })

                defaultVisibleColumn.forEach(id => {
                    selectedColumnCopy[id] = true
                })

                return selectedColumnCopy
            })
        }
    }, [])

    return (
        <Box sx={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
            {
                !withSearch
                    ? <Box/>
                    : <SearchInput
                        tooltipPlacement={tooltipPlacement}
                        tooltipTitle={tooltipTitle}
                        value={filterValue}
                        onChange={onSearchInput}
                    />
            }
            <Box sx={{display: 'flex', gap: '10px', alignItems: 'center'}}>
                {children}
                {
                    withManageColumn &&
                    <ManageColumnButton
                        visibleColumn={visibleColumn}
                        onToggleColumn={onToggleColumn}
                        onToggleAllColumn={onToggleAllColumn}
                        cellsProps={dataCellProps}
                    />
                }
            </Box>
        </Box>
    )
}

Banner.customFuncName = BANNER_CHILD_NAME;

Banner.propTypes = {
    tooltipTitle: PropTypes.string,
    tooltipPlacement: PropTypes.string,
    filterValue: PropTypes.string,
    defferFilterValue: PropTypes.string,
    onSearchInput: PropTypes.func,
    onFilter: PropTypes.func,
    findIntersection: PropTypes.func,
    data: PropTypes.array,
    keys: PropTypes.array,
    children: PropTypes.any
}

export default Banner;