import {RouterProvider} from "react-router-dom";

import {ThemeProvider} from "@mui/material";

import {router} from '@src/shared/config/router'
import {ErrorBoundary} from "./providers/errorBoundary";
import {theme} from './theme'

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
