import Admin from '../pages/Admin';
import Dashboard from '../pages/Dashboard';
import ErrorPage from '../pages/ErrorPage';
import Items from '../pages/Items';
import Layout from '../pages/Layout';
import UserSettings from '../pages/UserSettings';

export default function privateRoutes() {

    return {
        path: '/',
        element: <Layout />,
        errorElement: <ErrorPage />,
        children: [
            { path: '/', element: <Dashboard /> },
            { path: 'items', element: <Items /> },
            { path: 'admin', element: <Admin /> },
            { path: 'settings', element: <UserSettings /> },
        ],
    };
}
