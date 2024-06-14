import {RootState} from "@src/shared/model/store";

export const menuSelector = (state: RootState) => state.menu;

export const isMenuOpenSelector = (state: RootState) => menuSelector(state).isMenuOpen

export const activePageIdSelector = (state: RootState) => menuSelector(state).activePageId

export const activeMenuTabIdSelector = (state: RootState) => menuSelector(state).activeMenuTabId

export const openedTabsSelector = (state: RootState) => menuSelector(state).openedTabs
