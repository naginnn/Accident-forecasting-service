import React from 'react';
import {RouterProvider} from "react-router-dom";

import {createTheme, ThemeProvider} from "@mui/material";

import router from './router'
import ErrorBoundary from "./ErrorBoundary";

const theme = createTheme({
    typography: {
        button: {
            textTransform: 'none',
            fontSize: '17px'
        }
    },
    components: {
        MuiTableRow: {
            styleOverrides: {
                root: {
                    '&:last-child td, &last-child th': {border: 0}
                }
            }
        }
    }
})

// Точка инициализации
function App() {
  return (
      <ErrorBoundary>
          <ThemeProvider theme={theme}>
              <RouterProvider router={router}/>
          </ThemeProvider>
      </ErrorBoundary>
  );
}

export default App;
