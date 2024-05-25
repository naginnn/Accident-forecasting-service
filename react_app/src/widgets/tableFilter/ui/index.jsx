import {useState, Children, cloneElement, useDeferredValue, useRef, useLayoutEffect} from "react";

import {TableContainer, TablePagination, Table, TableRow, TableHead, Box} from "@mui/material";


import {DefaultTableBody} from "./defaultTableBody/DefaultTableBody";
import {SortCell} from "./filterCells/sortCell/SortCell";
import {SelectCell} from "./filterCells/selectCell/SelectCell";
import {ToggleCell} from "./filterCells/toggleCell/ToggleCell";
import {BaseCell} from "./filterCells/baseCell/BaseCell";
import {Banner} from "./banner/Banner";

import {useSortFilter} from "../hooks/useSortFilter";
import {usePagination} from "../hooks/usePagination";

import {
    BANNER_CHILD_NAME,
    BASE_CELL_CHILD_NAME,
    SELECT_CELL_CHILD_NAME,
    SORT_CELL_CHILD_NAME,
    TOGGLE_CELL_CHILD_NAME,
} from "../const/CellNames";

import {
    SessionStorageManager,
} from '../utils/sessionStorageManager'

// Получает пропсы Cell children
const getDataCellProps = (childrenCells) => {
    const cellProps = []

    Children.forEach(childrenCells, childCell => {
        if (childCell?.type?.customFuncName && childCell?.type?.customFuncName !== BANNER_CHILD_NAME) {
            cellProps.push(childCell.props)
        }
    })

    return cellProps
}

const getAllVisibleColumns = (childrenCells) => {
    const column = {}
    const props = getDataCellProps(childrenCells)

    props.forEach(cellProps => column[cellProps.id] = true)

    return column
}

// При ререндере родительского компонента в котором расположена таблица
// изменяется children, здесь мы сравниваем идентичность предыдущих children и текущих
// если children изменился возвращаем новые колонки
const isChildrenIdentical = (currChildrenId, prevChildrenID) => {
    if (prevChildrenID) {
        const prevCellsId = Object.keys(prevChildrenID)
        const currCellsId = Object.keys(currChildrenId)

        if (prevCellsId.length === currCellsId.length && prevCellsId.every(cellId => cellId in currChildrenId))
            return true
    }
    return false
}

// Сортирует таблицу в зависимости от выбранных опций в SelectCell
// и направлению сортировки asc/desc в SortCell
// onFilter, onChangePagination - функции которая передает фильтрованные данные наверх, должна быть обернута в useCallback
// id в children должен передаваться если мы используем флаг withManageColumn в компоненту tableFilter.Banner
// paperWrapperProps - пропсы для PaperWrapper
// rowsPerPageInit - кол-во эл-в в таблице, если есть пагинация
export const TableFilter = ({
                         data,
                         withPagination,
                         onFilter,
                         onChangePagination,
                         getTableBodyLayout,
                         id,
                         sx,
                         rowsPerPageInit,
                         children
                     }) => {
    const [filteredData, setFilteredData] = useState(data)

    const isFirstRender = useRef(true)

    // Получаем все ключе столбцов для отрисовки дефолтной верстки строки
    const [dataCellProps, setDataCellProps] = useState(() => getDataCellProps(children))

    const [withManageColumn, setWithManageColumn] = useState(false)
    const [visibleColumn, setVisibleColumn] = useState(() => {
        const visibleColumns = getAllVisibleColumns(children)
        const joinedVisColSessionStorage = SessionStorageManager.getVisibleColumnsValue(id, visibleColumns)

        return joinedVisColSessionStorage
    })
    const [withSearch, setWithSearch] = useState(false)
    const [searchFilter, setSearchFilter] = useState(() => SessionStorageManager.getSearchValue(id));
    const [customFindIntersection, setCustomFindIntersection] = useState(false)
    const deferredFilterSearch = useDeferredValue(searchFilter);

    const [selectedCell, setSelectedCell] = useState([]) // тип: [{keyName: '', options: []0}]

    const {sort, sortOrderBy, sortFieldKey, onToggle} = useSortFilter(id);

    const onChangeInnerPagination = (getPage, rowsPerPage, getPageContent) => {
        if (onChangePagination && typeof onChangePagination === 'function') {
            onChangePagination(getPage(filteredData), rowsPerPage, getPageContent(filteredData))
        }
    }

    const {onChangePage, getPageContent, rowsPerPage, сhangeRowsPerPage, getPage} = usePagination({
        tableId: id,
        onChangePagination: onChangeInnerPagination,
        data: filteredData,
        rowsPerPageInit
    });

    // Фильтрация данных по поискову значению, используются если не передана функция в props
    // Берет все ключи в объекте и осуществляет поиск по каждой из них
    const defaultFindIntersection = (data, searchValue, withManageColumn, visibleKeyNamesObj) => {
        const filterLowCase = searchValue.toLowerCase().trim();
        let filteredData = data

        if (filterLowCase && data.length) {
            const keys = Object.keys(data[0]).filter(key => {
                // Удаляем ключи которые не видны на странице, чтобы по ним не велся поиск
                if (withManageColumn && !(key in visibleKeyNamesObj)) return false

                return true
            })

            filteredData = data.filter(el => {
                let findIntersection = false
                for (let key of keys) {
                    if (typeof el[key] === 'string' && el[key]?.toLowerCase().trim().includes(filterLowCase)) {
                        findIntersection = true

                        break;
                    }
                }

                return findIntersection
            })
        }

        return filteredData
    }

    // Манипуляция селекционнами опциями столбцов
    const onChangeSelectOpt = (cellName, options) => {
        const newSelectedCell = selectedCell.findIndex(opt => opt.keyName == cellName) // ищем фильтруется ли уже эта ячейка

        if (!~newSelectedCell && !options.length) // не было ячейки и опций нет (1 рендер)
            return;

        setSelectedCell((selectedCell) => {
            if (!options.length && ~newSelectedCell) { // фильтруется, но опций нет - удаляем из фильтрующихся ячеек
                return selectedCell.filter(opt => opt.keyName != cellName)
            } else if (~newSelectedCell) { // ячейка фильтровалась - добавляем новые опции
                return selectedCell.map(opt => opt.keyName == cellName ? {...opt, options} : opt)
            } else { // ячейка не фильтровалась - добавляем новую ячейку с опциями
                return [...selectedCell, {keyName: cellName, options}]
            }
        });
    }

    // Обработка изменения поисково  строки
    const onSearchInput = (e) => {
        SessionStorageManager.setSearchValue(id, e.target.value)
        setSearchFilter(e.target.value)
    }

    // Основная функция фильтрации данных по всем параметрам
    const onInnerFilterData = () => {
        let filteredData = data

        // Определение видимых колонок
        const visibleKeyNamesArr = withManageColumn && Object.entries(visibleColumn).filter(([id, isVisible]) => isVisible).map(([id, isVisible]) => {
            let keyName

            Children.forEach(children, child => {
                if (child?.props?.id === id) {
                    keyName = child?.props?.keyName
                }
            })

            return [keyName, isVisible]
        }).filter(([keyName]) => keyName)
        const visibleKeyNamesObj = withManageColumn && Object.fromEntries(visibleKeyNamesArr)

        // Фильтрация по селекционны ячейкам
        filteredData = filteredData.filter(data => {
            return selectedCell.every(({options, keyName}) => {
                if (withManageColumn && !(keyName in visibleKeyNamesObj)) // Если ячейка невидимая, то не включаем ее в сортировку
                    return true

                return options.some(option => {
                    if (typeof data[keyName] === 'boolean' && (option === 'false' || option === 'true')) {
                        return option === `${data[keyName]}`
                    }

                    return option == data[keyName]
                })
            })
        })

        // asc/desc сортировка
        if (sortFieldKey && sortOrderBy) {
            // Если есть управлением кол-ва колонок и колонка видимая или нет управление колонками - сортировка
            if (!withManageColumn || (withManageColumn && sortFieldKey in visibleKeyNamesObj))
                filteredData = sort(filteredData)
        }

        // сортировка по поиску
        if (deferredFilterSearch && withSearch) {
            if (customFindIntersection) {
                filteredData = customFindIntersection(filteredData, deferredFilterSearch)
            } else {
                filteredData = defaultFindIntersection(filteredData, deferredFilterSearch, withManageColumn, visibleKeyNamesObj)
            }
        }

        setFilteredData(filteredData)

        // Передаем данные наружу компонента
        if (onFilter && typeof onFilter === 'function') {
            onFilter(filteredData)
        }
    }

    // Обновляет отфильтрованные данные и пропсы ячеек заголовков
    // в случае изменения даты или children
    useLayoutEffect(() => {
        if (isFirstRender.current) {
            isFirstRender.current = false
        } else {
            setDataCellProps(() => getDataCellProps(children, true))
            if (withManageColumn)
                setVisibleColumn((prevVisible) => {
                    const currVisible = getAllVisibleColumns(children)
                    if (isChildrenIdentical(currVisible, prevVisible))
                        return prevVisible

                    const joinedVisColSessionStorage = SessionStorageManager.getVisibleColumnsValue(id, currVisible)
                    SessionStorageManager.setVisibleColumnsValue(id, joinedVisColSessionStorage)
                    return currVisible
                })

            onInnerFilterData()
        }
    }, [children, data])

    // Сортировка данных, очередность сортировки
    // 1 - по селекционным ячейкам, 2 - по направлению asc / desc, 3 - по поиску
    useLayoutEffect(() => {
        onInnerFilterData()
    }, [sortFieldKey, sortOrderBy, deferredFilterSearch, selectedCell, visibleColumn, withManageColumn])

    return (
        <Box sx={{overflow: sx?.overflow || 'auto'}}>
            <TableContainer sx={{minWidth: sx?.minWidth || '100%', py: '5px' ,...sx}}>
                    {
                        // Поиск в поиске ведется только из фильтрованных данных по селекту
                        Children.map(children, child => {
                            if (child?.type?.customFuncName === BANNER_CHILD_NAME) {
                                return cloneElement(child, {
                                    setCustomIntersection: setCustomFindIntersection,
                                    setWithManageColumnOuter: setWithManageColumn,
                                    setWithSearchOuter: setWithSearch,
                                    visibleColumn: visibleColumn,
                                    setVisibleColumn: setVisibleColumn,
                                    dataCellProps: dataCellProps,
                                    filterValue: searchFilter,
                                    tableId: id,
                                    onSearchInput,
                                })
                            }

                            return null;
                        })
                    }
                    <Table
                        sx={{
                            tableLayout: 'fixed',
                            wordBreak: 'break-word',
                            '.MuiTableBody-root': {
                                '.MuiTableRow-root': {
                                    '.MuiTableCell-root': {
                                        px: '8px' // Устанавливает padding-x в ячейках tableBody
                                    }
                                }
                            }
                        }}
                        size='small'
                    >
                        <TableHead sx={{wordBreak: 'normal'}}>
                            <TableRow>
                                {
                                    // остальная часть пропсов в компонент прокидывается выше
                                    // пример <TableFilterSkeleton.SortCell topic='' keyName=''/>
                                    Children.map(children, child => {

                                        // Если колонки сортируются, проверяем все ячейки (исключаем баннер)
                                        // Проверяем есть ли id ячейки в показываемых колонках, если колонка спрятана, возвращаем null
                                        if (withManageColumn
                                            && child?.type?.customFuncName !== BANNER_CHILD_NAME
                                            && child?.props?.id in visibleColumn
                                            && !visibleColumn[child?.props?.id])
                                            return null

                                        switch (child?.type?.customFuncName) {
                                            case SORT_CELL_CHILD_NAME :
                                                return cloneElement(child, {
                                                    onToggle,
                                                    sortOrderBy,
                                                    activeName: sortFieldKey,
                                                    onChangePage: withPagination && onChangePage
                                                })
                                            case SELECT_CELL_CHILD_NAME:
                                                return cloneElement(child, {
                                                    data,
                                                    onFilter: onChangeSelectOpt,
                                                    tableId: id
                                                })
                                            case TOGGLE_CELL_CHILD_NAME:
                                                return cloneElement(child, {
                                                    data,
                                                    tableId: id,
                                                    onFilter: onChangeSelectOpt,
                                                })
                                            case BASE_CELL_CHILD_NAME:
                                                return child
                                            default:
                                                return null;
                                        }
                                    })
                                }
                            </TableRow>
                        </TableHead>
                        {
                            getTableBodyLayout
                                ? getTableBodyLayout(filteredData, getPageContent, withManageColumn && visibleColumn)
                                : <DefaultTableBody
                                    getPageContent={getPageContent}
                                    data={filteredData}
                                    cellProps={dataCellProps}
                                    visibleColumn={withManageColumn && visibleColumn}
                                />
                        }
                    </Table>
                {
                    withPagination &&
                    filteredData &&
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 15, 20, 30]}
                        component="div"
                        count={filteredData.length}
                        page={getPage(filteredData)}
                        rowsPerPage={rowsPerPage}
                        labelRowsPerPage=''
                        onRowsPerPageChange={сhangeRowsPerPage}
                        onPageChange={onChangePage}
                    />
                }
            </TableContainer>
        </Box>
    )
}

TableFilter[BANNER_CHILD_NAME] = Banner;
TableFilter[SORT_CELL_CHILD_NAME] = SortCell;
TableFilter[SELECT_CELL_CHILD_NAME] = SelectCell;
TableFilter[TOGGLE_CELL_CHILD_NAME] = ToggleCell;
TableFilter[BASE_CELL_CHILD_NAME] = BaseCell;
