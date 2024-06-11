declare module '*module.scss'
declare module '*module.css'

import { YMap } from 'ymaps3'

declare let map: YMap

declare global {
    interface Window {
        map: YMap | null
    }
}
