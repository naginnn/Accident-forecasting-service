import dayjs from "dayjs";

// принимает массив объектов, имя ключа где хранится время,
// информация о мутабельности массива (если он иммутабельный, нужно делать копию)
// !!! направление сортировки 'asc', 'desc'
export const sortArrOfObjByTime = (
    arr: any[],
    keyName: string,
    direction: 'asc' | 'desc' = 'asc',
) => {
    const withData = arr.filter((obj: any) => {
        if (!(keyName in obj)) throw new Error('Нет такого ключа в объекте')

        return typeof obj[keyName] === 'string'
    })
    const emptyData = arr.filter((obj: any) => typeof obj[keyName] !== 'string')
    const sortDirection = direction === 'desc' ? 1 : -1

    const sortedData = withData.sort((a: any, b: any) => {
        const dataA = Date.parse(dayjs(a[keyName]).format('YYYY-MM-DDTHH:mm:ss.sssZ'));
        const dataB = Date.parse(dayjs(b[keyName]).format('YYYY-MM-DDTHH:mm:ss.sssZ'));

        // делает сортировку стабильной
        if (dataA === dataB)
            return a;

        return (dataA > dataB ? -1 : 1) * sortDirection;
    })

    return [...sortedData, ...emptyData]
}
