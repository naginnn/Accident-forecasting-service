type SerializeValue = boolean | 'да' | 'нет'

// Переименовывает boolean значение в строку и наоборот,
// пример: true => 'нет' и наоборот
export const renameBoolean = (value: SerializeValue) => {
    switch (value) {
        case false:
            return 'нет'
        case true:
            return 'да'
        case 'нет':
            return false
        case 'да':
            return true
        default: {
            const exception: never = value;
            return exception
        }
    }
}
