import React from 'react';
import ReactDOM from 'react-dom/client';

import { ChakraProvider } from '@chakra-ui/provider';
import { createStandaloneToast } from '@chakra-ui/toast';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import { OpenAPI } from './client';
import { isLoggedIn } from './hooks/useAuth';
import privateRoutes from './routes/private_route';
import publicRoutes from './routes/public_route';
import theme from './theme';


OpenAPI.BASE = import.meta.env.VITE_API_URL;
OpenAPI.TOKEN = async () => {
  return localStorage.getItem('access_token') || '';
}

const router = createBrowserRouter([
  isLoggedIn() ? privateRoutes() : {},
  ...publicRoutes(),
]);

const { ToastContainer } = createStandaloneToast();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <RouterProvider router={router} />
      <ToastContainer />
    </ChakraProvider>
  </React.StrictMode>,
)

