import React from 'react';
import ReactDOM from 'react-dom/client';

import { ChakraProvider } from '@chakra-ui/provider';
import { createStandaloneToast } from '@chakra-ui/toast';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import { OpenAPI } from './client';
import Admin from './pages/Admin';
import Dashboard from './pages/Dashboard';
import ErrorPage from './pages/ErrorPage';
import Items from './pages/Items';
import Login from './pages/Login';
import RecoverPassword from './pages/RecoverPassword';
import Root from './pages/Root';
import Profile from './pages/UserSettings';
import theme from './theme';


OpenAPI.BASE = import.meta.env.VITE_API_URL;
OpenAPI.TOKEN = async () => {
  return localStorage.getItem('access_token') || '';
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      { path: '/', element: <Dashboard /> },
      { path: 'items', element: <Items /> },
      { path: 'admin', element: <Admin /> },
      { path: 'settings', element: <Profile /> },
    ],
  },
  { path: 'login', element: <Login />, errorElement: <ErrorPage />, },
  { path: 'recover-password', element: <RecoverPassword />, errorElement: <ErrorPage />, },
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

