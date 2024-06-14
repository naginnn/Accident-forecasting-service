import dayjs from "dayjs";

// Фун-я преобразования даты в другой формат
// TODO обернуть в try-catch
export const transformDateFormat = (date: any, format: string): string => {
    return dayjs(date).format(format)
}