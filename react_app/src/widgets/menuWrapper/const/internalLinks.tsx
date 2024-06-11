import GiteIcon from '@mui/icons-material/Gite';

export const menuLinkTopics = {
    CONSUMERS: 'Потребители'
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
}

export const internalLinks: InternalLinkT[] = [
    {
        id: linkTopicIdConnect[menuLinkTopics.CONSUMERS].id,
        topic: linkTopicIdConnect[menuLinkTopics.CONSUMERS].topic,
        icon: <GiteIcon/>,
        url: '/consumers',
    }
]