import {useEffect} from "react";

import {useAppDispatch} from "@src/shared/model/store";


import {setActiveMenuTabId} from "../store";
import {linkTopicIdConnect, MenuLinkTopics} from "../const/internalLinks";
import {MenuWrapper} from "../ui/MenuWrapper";

export function withMenu<P extends object>(Component: React.ComponentType<P>, menuLinkTopic: MenuLinkTopics) {
    const displayName = Component.displayName || Component.name || "Component"

    const ComponentWithAuth = (props: P) => {
        const dispatch = useAppDispatch();

        useEffect(() => {
            dispatch(setActiveMenuTabId(linkTopicIdConnect[menuLinkTopic].id))
        }, [dispatch]);

        return <MenuWrapper>
            <Component {...props}/>
        </MenuWrapper>
    }

    ComponentWithAuth.displayName = `withMenu(${displayName})`

    return ComponentWithAuth
}