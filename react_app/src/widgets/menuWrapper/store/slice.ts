import {createSlice} from '@reduxjs/toolkit'
import type {PayloadAction} from '@reduxjs/toolkit'

const NAME = 'menu';

interface IAppState {
    isMenuOpen: boolean
    activePageId: string
    activeMenuTabId: string
    openedTabs: Record<string, boolean>
}

const initialState: IAppState = {
    isMenuOpen: false,
    activePageId: '',
    activeMenuTabId: '',
    openedTabs: {}
}

const onToggleMenuState = (state: IAppState) => {
    state.isMenuOpen = !state.isMenuOpen
}

const setActivePageId = (state: IAppState, action: PayloadAction<string>) => {
    state.activePageId = action.payload
}

const setActiveMenuTabId = (state: IAppState, action: PayloadAction<string>) => {
    state.activeMenuTabId = action.payload
}

const toggleOpenTabs = (state: IAppState, action: PayloadAction<string>) => {
    const copyTabs = JSON.parse(JSON.stringify(state.openedTabs))

    if (action.payload in copyTabs) {
        delete copyTabs[action.payload]
    } else {
        copyTabs[action.payload] = true
    }

    state.openedTabs = copyTabs
}

export const {reducer: menuReducer, actions: menuActions} = createSlice({
    name: NAME,
    initialState,
    reducers: {
        onToggleMenuState,
        setActivePageId,
        setActiveMenuTabId,
        toggleOpenTabs
    },
})
