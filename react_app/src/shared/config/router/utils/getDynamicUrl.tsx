export const getDynamicUrl = (link: string, ...params: Array<string | undefined> ) => {
    for (let i = 0; i < params.length; i++) {
        if (typeof params[i] === 'undefined') return link
    }

    const urlSemgents = link.split('/')
    const numDynamicParams = urlSemgents.reduce((prev, curr) => {
        return curr.startsWith(':') ? ++prev : prev
    }, 0)

    if (numDynamicParams !== params.length) {
        throw new Error('Неверное количество параметров для создания url')
    }

    let paramInd = 0
    return urlSemgents.map(urlPart => {
        if (urlPart.startsWith(':')) {
            return params[paramInd++]
        }

        return urlPart
    }).join('/')
}
