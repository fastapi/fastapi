import ErrorPage from '../pages/ErrorPage';
import Login from '../pages/Login';
import RecoverPassword from '../pages/RecoverPassword';

export default function publicRoutes() {
    return [
        { path: '/login', element: <Login />, errorElement: <ErrorPage /> },
        { path: 'recover-password', element: <RecoverPassword />, errorElement: <ErrorPage /> },
        // TODO: complete this
        // { path: '*', element: <Navigate to='/login' replace /> }
    ];
}

