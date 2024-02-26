import { useUserStore } from '../store/user-store';
import { Body_login_login_access_token as AccessToken, LoginService } from '../client';
import { useUsersStore } from '../store/users-store';
import { useItemsStore } from '../store/items-store';

const useAuth = () => {
    const { user, getUser, resetUser } = useUserStore();
    const { resetUsers } = useUsersStore();
    const { resetItems } = useItemsStore();

    const login = async (data: AccessToken) => {
        const response = await LoginService.loginAccessToken({
            formData: data,
        });
        localStorage.setItem('access_token', response.access_token);
        await getUser();
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        resetUser();
        resetUsers();
        resetItems();
    };

    const isLoggedIn = () => {
        return user !== null;
    };

    return { login, logout, isLoggedIn };
}

export default useAuth;