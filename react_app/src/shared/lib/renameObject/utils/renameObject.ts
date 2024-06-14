import {renameBoolean} from "./renameBoolean";

// Фун-я переименования ключей объекта и boolean значений, создает новый объект, но значения внутри не копирует
// new_names - новые имена для ключей originObject, где ключи new_names совпадают с ключами
// originObject, а значение new_names являются переводом для ключей originObject. См. пример в тестах
// originObject - объект в котором меняются ключи
// renameBoolean - флаг, при значение true перименовывает boolean значения
export const renameObject = (new_names: Record<string, string> | undefined, originObject: Record<string, any> | undefined, renameBool = false) => {
    if (!new_names && originObject) {
        return originObject
    } else if (!originObject || !new_names) {
        return {}
    }

    const res: Record<string, any> = {};

    Object.keys(new_names).forEach(new_key => {
        if (new_key in originObject) {
            res[new_names[new_key]] = originObject[new_key];
        }
    })

    // TODO лучше вынести в отдельный функцию и убрать от сюда
    // так как функция renameObject отвечает за переименование ключей объекта
    // а не значений объекта
    if (renameBool) {
        Object.keys(res).forEach(key => {
            if (typeof res[key] === 'boolean' || res[key] === 'нет' || res[key] === 'да')
                res[key] = renameBoolean(res[key]);
        })
    }

    return res;
}