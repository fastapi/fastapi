import { IUserProfile } from '@/interfaces';
import { AdminState } from './state';

export const mutations = {
    setUsers(state: AdminState, payload: IUserProfile[]) {
        state.users = payload;
    },
    setUser(state: AdminState, payload: IUserProfile) {
        const users = state.users.filter((user: IUserProfile) => user.name !== payload.name);
        users.push(payload);
        state.users = users;
    },
    setRoles(state: AdminState, payload: string[]) {
        state.roles = payload;
    },
};
