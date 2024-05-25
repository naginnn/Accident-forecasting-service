interface ISortValueType {
    keyName: string | undefined
    orderBy: string | undefined
    isTimeData: string | undefined
}

interface IPaginationValue {
    page: undefined | string
    rowsPerPage: undefined | string
}

export class SessionStorageManager {
    static getSearchValue = (tableId: string | undefined) => {
        if (!tableId) return ''

        return sessionStorage.getItem(`table:${tableId};searchInput`) || ''
    }

    static setSearchValue = (tableId: string | undefined, value: string) => {
        if (tableId) {
            if (!value) {
                sessionStorage.removeItem(`table:${tableId};searchInput`)
            } else {
                sessionStorage.setItem(`table:${tableId};searchInput`, value)
            }
        }
    }

    static getSortValue = (tableId: string | undefined): ISortValueType => {
        if (tableId) {
            const sortInfo = sessionStorage.getItem(`table:${tableId};sortCell`)?.split(';')

            if (sortInfo && sortInfo.length === 3) {
                return {
                    keyName: sortInfo[0],
                    orderBy: sortInfo[1],
                    isTimeData: sortInfo[2]
                }
            }
        }

        return {
            keyName: undefined,
            orderBy: undefined,
            isTimeData: undefined
        }
    }

    static setSortValue = (tableId: string | undefined, cellName: string, sortDirections: 'asc' | 'desc', isTimeData: boolean) => {
        if (tableId) {
            sessionStorage.setItem(`table:${tableId};sortCell`, `${cellName};${sortDirections};${isTimeData}`)
        }
    }

    static setPaginationValue = (tableId: string | undefined, page: number, rowsPerPage: number) => {
        if (tableId) {
            sessionStorage.setItem(`table:${tableId};pagination`, `${page};${rowsPerPage}`)
        }
    }

    static getPaginationValue = (tableId: string | undefined): IPaginationValue => {
        const paginationInfo: IPaginationValue = {
            page: undefined,
            rowsPerPage: undefined
        }

        if (tableId) {
            const info = sessionStorage.getItem(`table:${tableId};pagination`)?.split(';')

            if (info && info.length === 2) {
                paginationInfo.page = info[0]
                paginationInfo.rowsPerPage = info[1]
            }
        }

        return paginationInfo
    }

    static setSelectCellValue = (tableId: string | undefined, cellName: string, cellValue: string[]) => {
        if (tableId && Array.isArray(cellValue)) {
            if (cellValue.length) {
                sessionStorage.setItem(`table:${tableId};selectCell:${cellName}`, cellValue.join(';'))
            } else {
                sessionStorage.removeItem(`table:${tableId};selectCell:${cellName}`)
            }
        }
    }

    static getSelectCellValue = (tableId: string | undefined, cellName: string): string[] => {
        let values: string[] = []

        if (tableId) {
            values = sessionStorage.getItem(`table:${tableId};selectCell:${cellName}`)?.split(';') || []
        }

        return values
    }

    static setVisibleColumnsValue = (tableId: string | undefined, columns: { [id: string]: boolean }) => {
        if (tableId) {
            const key = `table:${tableId};visibleCell`

            const unVisibleColumns = Object.entries(columns)
                .filter(([id, isVisible]) => !isVisible)
                .map(([id, isVisible]) => id)

            if (unVisibleColumns.length) {
                sessionStorage.setItem(key, unVisibleColumns.join(';'))
            } else if (!unVisibleColumns.length && sessionStorage.getItem(key)) {
                sessionStorage.removeItem(key)
            }
        }
    }

    static getUnvisibleColumnsVal = (tableId: string): string[] => {
        return sessionStorage.getItem(`table:${tableId};visibleCell`)?.split(';') || []
    }

    static getVisibleColumnsValue = (tableId: string | undefined, columns: { [id: string]: boolean }) => {
        if (tableId) {
            const unVisibleColumns = this.getUnvisibleColumnsVal(tableId)

            unVisibleColumns.forEach(id => columns[id] = false)
            return columns
        }
        return columns
    }
}
