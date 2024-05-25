// принимает массив объектов, имя ключа
// информация о мутабельности массива (если он иммутабельный, нужно делать копию)
// !!! направление сортировки 'asc', 'desc'
export const sortArr = <T extends {[x: string]: any}>(
    arr: Array<T>,
    keyName: string,
    direction: 'asc' | 'desc' = 'asc',
    isImmutableArr: boolean = false
) => {
    const copyArr: Array<T> = isImmutableArr ? JSON.parse(JSON.stringify(arr)) : arr;
    const sortDirection = direction === 'desc' ? 1 : -1

    return copyArr.sort((a: T, b: T) => {
        if (!(keyName in a) || !(keyName in b)) throw new Error('Нет такого ключа в объекте')

        // делает сортировку стабильной
        if (a[keyName] === b[keyName])
            return 1;

        return (a[keyName] > b[keyName] ? -1 : 1) * sortDirection;
    })
}
