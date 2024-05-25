import {useState, useMemo, useEffect, useDeferredValue, useCallback} from "react";

import {BaseCell} from "../baseCell/BaseCell";
import {Options} from "./Options"

import {SessionStorageManager} from "../../../utils/sessionStorageManager";

import {SELECT_CELL_CHILD_NAME} from "../../../const/CellNames";

export const ALL_OPTIONS_NAME = 'Все'

// Сортирует таблицу согласно выбранным уникальным значениям
// Принимает данные и ключ, название ячейки
// booleanName - массив из 2 элементов, 1 элемент - название для true, 2 для false ['Да', 'Нет']
// defaultCheckedOptions - дефолтные выбранные опции массив строк
const SelectCell = (
    {
        topic,
        data,
        keyName,
        tableId,
        booleanName,
        defaultCheckedOptions = [],
        onFilter,
        sx,
        ...props
    }) => {
    // проходимся по массиву данных и собираем уникальные значения поля
    // также добляем опцию "ALL"
    const options = useMemo(() => {
        const uniqOptions = {[ALL_OPTIONS_NAME]: true}
        let hasBooleanVal = false

        data.forEach((el) => {
            if (keyName in el && typeof el[keyName] !== 'object') {
                const val = typeof el[keyName] === 'string' ? el[keyName] : String(el[keyName])

                if (typeof val === 'boolean')
                    hasBooleanVal = true

                uniqOptions[val] = true
            }
        })

        // Если передали booleanName, то их опции всегда отображаем в списке опций
        if (booleanName || hasBooleanVal) {
            uniqOptions['true'] = true
            uniqOptions['false'] = true
        }

        return Object.keys(uniqOptions);
    }, [data, keyName])

    const isAllOptionSelected = (allOptions, selectedOptions) => {
        const withoutAllSelected = selectedOptions.filter(opt => opt !== ALL_OPTIONS_NAME)

        return withoutAllSelected.length >= allOptions.length - 1 ? true : false
    }

    const initSelectedOptions = () => {
        const allUniqSelectedOpt = {}
        const prevSelectedOpt = SessionStorageManager.getSelectCellValue(tableId, keyName)

        defaultCheckedOptions.forEach(opt => allUniqSelectedOpt[opt] = true)
        prevSelectedOpt.forEach(opt => allUniqSelectedOpt[opt] = true)

        const allSelectedOpt = Object.keys(allUniqSelectedOpt)
        return (allSelectedOpt.length && !isAllOptionSelected(options, allSelectedOpt)) ? allSelectedOpt : options
    }

    // Инициализируем выбранные опции из defaultCheckedOptions, которые передаются через пропсы и
    // из предыдущих выбранных опций, которые хранятся в sessionStorage (работает если только передан tableId),
    // если дефолтных и предыдущих опций нет, то выбираем все опции выбранными
    const [selectedOpt, setSelectedOpt] = useState(() => {
        return initSelectedOptions()
    })

    const deferredSelectedOpt = useDeferredValue(selectedOpt);

    // если нет уникальных опциий, то обнуляется выбранные опции
    useEffect(() => {
        if (!options.length && deferredSelectedOpt.length) {
            SessionStorageManager.setSelectCellValue(tableId, keyName, [])
            setSelectedOpt([])
        }
    }, [options, deferredSelectedOpt, setSelectedOpt])

    useEffect(() => {
        onFilter(keyName, deferredSelectedOpt)
    }, [deferredSelectedOpt, keyName])

    const onChangeSelectOpt = useCallback((option) => {
        let newOpt;
        let allOptionSelected;
        const optIndex = selectedOpt.findIndex((selectedOpt) => option == selectedOpt) // проверяет есть ли уже такая опция

        if (option === ALL_OPTIONS_NAME) {
            newOpt = ~optIndex ? [] : options
            allOptionSelected = true
        } else {
            newOpt = ~optIndex ? selectedOpt.filter((_, i) => i != optIndex) : [...selectedOpt, option]; // есть - удаляем, нет - добавляем
            allOptionSelected = isAllOptionSelected(options, newOpt)
            if (allOptionSelected) {
                newOpt = options
            } else {
                newOpt = newOpt.filter(opt => opt !== ALL_OPTIONS_NAME)
            }
        }

        // Если все опции выбраны и не было дефолтных выбранных опций
        // то обнуляем выбранные опции
        if (allOptionSelected && !defaultCheckedOptions.length) {
            SessionStorageManager.setSelectCellValue(tableId, keyName, [])
        } else {
            SessionStorageManager.setSelectCellValue(tableId, keyName, newOpt)
        }
        setSelectedOpt(newOpt)
    }, [options, selectedOpt, setSelectedOpt])

    return (
        <BaseCell
            sx={sx}
            topic={topic}
            filterIcon={
                <Options
                    options={options}
                    selectedOptions={selectedOpt}
                    booleanName={booleanName}
                    onChangeSelectOptions={onChangeSelectOpt}
                />
            }
            booleanName={booleanName}
            {...props}
        />
    )
}

SelectCell.customFuncName = SELECT_CELL_CHILD_NAME;

export {SelectCell}

