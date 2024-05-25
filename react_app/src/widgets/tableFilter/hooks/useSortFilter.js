import {useState} from "react";

import {toggle} from "@src/shared/lib/toggle";
import {sortArrOfObjByTime} from "@src/shared/lib/sortArrOfObjByTime"
import {sortArr} from "@src/shared/lib/sortArr";

import {SessionStorageManager} from "../utils/sessionStorageManager";

// Хук для сортировки массива объекта в порядке возрст/убыв
export const useSortFilter = (tableId) => {
    const [sortFieldKey, setSortFieldKey] = useState(() => {
        return SessionStorageManager.getSortValue(tableId).keyName
    });
    const [sortOrderBy, setOrderBy] = useState(() => {
        return SessionStorageManager.getSortValue(tableId).orderBy
    });
    const [isTime, setIsTime] = useState(() => {
        return SessionStorageManager.getSortValue(tableId).isTimeData
    });

    // Если поле содержит время, сортирует по времени
    const sort = (data) => {
        if (isTime) {
            return sortArrOfObjByTime(data, sortFieldKey, sortOrderBy)
        }

        return sortArr(data, sortFieldKey, sortOrderBy, true)
    }

    // Определяет направление сортировки.
    // Если новый фильтр является текущем - изменяет направление,
    // иначе обновляет имя фильтра и указывает возрастающее направление
    const onToggle = (key, isTimeData = false) => {
        setIsTime(isTimeData)

        if (sortFieldKey === key) {
            const newSortOrderBy = toggle(sortOrderBy, 'asc', 'desc')
            setOrderBy(newSortOrderBy)

            SessionStorageManager.setSortValue(tableId, key, newSortOrderBy, isTimeData)
            return
        }

        setSortFieldKey(key);
        setOrderBy('asc');
        SessionStorageManager.setSortValue(tableId, key, 'asc', isTimeData)
    }

    return {sort, sortOrderBy, sortFieldKey, onToggle};
}
