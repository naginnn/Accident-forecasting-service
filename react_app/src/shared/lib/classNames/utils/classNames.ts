type Mods = Record<string, string | boolean>

export const classNames = (cls: string = '', mods: Mods = {}, additional: string[] = []): string => {
    return [
        cls,
        ...Object.entries(mods)
            .filter(([className, val]) => Boolean(val))
            .map(([className]) => className),
        ...additional.filter(Boolean)
    ].join(' ').trim()
}