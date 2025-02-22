import {Provider} from "react-redux";
import {RouterProvider} from "react-router-dom";
import {SnackbarProvider} from "notistack";

import {ThemeProvider} from "@mui/material";

import {router} from '@src/shared/config/router'
import {store} from '@src/shared/model/store'
import {NotistackAlert} from "@src/shared/ui/notistackAlert";
import {ErrorBoundary} from "@src/shared/ui/errorBoundary";

import {ErrorLayout} from "@src/entities/errorWrapper";

import {theme} from './theme'

// Точка инициализации
function App() {
    return (
        <ErrorBoundary fallback={<ErrorLayout/>}>
            <Provider store={store}>
                <SnackbarProvider
                    autoHideDuration={5000}
                    preventDuplicate
                    maxSnack={4}
                    Components={{
                        error: NotistackAlert,
                        success: NotistackAlert
                    }}
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'right',
                    }}
                >
                <ThemeProvider theme={theme}>
                    <RouterProvider router={router}/>
                </ThemeProvider>
                </SnackbarProvider>
            </Provider>
        </ErrorBoundary>
    );
}

export default App;
