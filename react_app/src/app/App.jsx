import {Provider} from "react-redux";
import {RouterProvider} from "react-router-dom";

import {ThemeProvider} from "@mui/material";

import {router} from '@src/shared/config/router'
import {store} from '@src/shared/model/store'

import {ErrorBoundary} from "./providers/errorBoundary";
import {theme} from './theme'

// Точка инициализации
function App() {
    return (
        <ErrorBoundary>
            <Provider store={store}>
                <ThemeProvider theme={theme}>
                    <RouterProvider router={router}/>
                </ThemeProvider>
            </Provider>
        </ErrorBoundary>
    );
}

export default App;
