import { AdminState } from './state';

export const getters = {
    adminUsers: (state: AdminState) => state.users,
    adminRoles: (state: AdminState) => state.roles,
    adminOneUser: (state: AdminState) => (name: string) => {
        const filteredUsers = state.users.filter((user) => user.name === name);
        if (filteredUsers.length > 0) {
            return { ...filteredUsers[0] };
        }
    },
};
