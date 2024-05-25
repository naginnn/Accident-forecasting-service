export type VisibleColumnT<T extends object> = {
    [K in keyof T]: boolean
}