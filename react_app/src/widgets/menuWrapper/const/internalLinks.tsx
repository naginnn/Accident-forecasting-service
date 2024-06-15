import GiteIcon from '@mui/icons-material/Gite';
import SettingsIcon from '@mui/icons-material/Settings';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';

export const menuLinkTopics = {
    CONSUMERS: 'Потребители',
    SETTINGS: 'Настройки',
    MODEL_INFO: 'Информация о модели'
} as const

export type MenuLinkTopics = (typeof menuLinkTopics)[keyof typeof menuLinkTopics]

interface BaseLink {
    topic: MenuLinkTopics
    id: string
}

export interface InternalLinkT extends BaseLink {
    topic: MenuLinkTopics
    icon: JSX.Element
    url: string
    extensiableLinks?: Array<Pick<InternalLinkT, 'topic' | 'url' | 'id'>>
}

export const linkTopicIdConnect: Record<MenuLinkTopics, BaseLink> = {
    'Потребители': {
        topic: 'Потребители',
        id: '0a2b7edd-5ba4-46b8-ab7e-dd5ba4f6b8e3'
    },
    'Настройки': {
        topic: 'Настройки',
        id: '1a2b7edd-5ba4-46b8-ab1e-dd5ba4f6b8e6'
    },
    'Информация о модели': {
        topic: 'Информация о модели',
        id: '1a2b2edd-5bk4-46b8-az1e-dd5ba4f6b8e6'
    }
}

export const internalLinks: InternalLinkT[] = [
    {
        id: linkTopicIdConnect[menuLinkTopics.CONSUMERS].id,
        topic: linkTopicIdConnect[menuLinkTopics.CONSUMERS].topic,
        icon: <GiteIcon/>,
        url: '/consumers',
    },
    {
        id: linkTopicIdConnect[menuLinkTopics.SETTINGS].id,
        topic: linkTopicIdConnect[menuLinkTopics.SETTINGS].topic,
        icon: <SettingsIcon/>,
        url: '/settings',
    },
    {
        id: linkTopicIdConnect[menuLinkTopics.MODEL_INFO].id,
        topic: linkTopicIdConnect[menuLinkTopics.MODEL_INFO].topic,
        icon: <InfoOutlinedIcon/>,
        url: '/model-info',
    }
]