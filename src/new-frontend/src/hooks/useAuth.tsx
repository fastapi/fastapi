import { useUserStore } from '../store/user-store';
import { Body_login_login_access_token as AccessToken, LoginService } from '../client';
import { useUsersStore } from '../store/users-store';
import { useItemsStore } from '../store/items-store';
import { useNavigate } from 'react-router-dom';

const isLoggedIn = () => {
    return localStorage.getItem('access_token') !== null;
};

const useAuth = () => {
    const { getUser, resetUser } = useUserStore();
    const { resetUsers } = useUsersStore();
    const { resetItems } = useItemsStore();
    const navigate = useNavigate();

    const login = async (data: AccessToken) => {
        const response = await LoginService.loginAccessToken({
            formData: data,
        });
        localStorage.setItem('access_token', response.access_token);
        await getUser();
        navigate('/');
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        resetUser();
        resetUsers();
        resetItems();
        navigate('/login');
    };

    return { login, logout };
}

export { isLoggedIn };
export default useAuth;