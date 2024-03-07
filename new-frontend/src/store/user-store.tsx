import { create } from 'zustand';
import { UpdatePassword, UserOut, UserUpdateMe, UsersService } from '../client';

interface UserStore {
    user: UserOut | null;
    getUser: () => Promise<void>;
    editUser: (user: UserUpdateMe) => Promise<void>;
    editPassword: (password: UpdatePassword) => Promise<void>;
    resetUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
    user: null,
    getUser: async () => {
        const user = await UsersService.readUserMe();
        set({ user });
    },
    editUser: async (user: UserUpdateMe) => {
        const updatedUser = await UsersService.updateUserMe({ requestBody: user });
        set((state) => ({ user: { ...state.user, ...updatedUser } }));
    },
    editPassword: async (password: UpdatePassword) => {
        await UsersService.updatePasswordMe({ requestBody: password });
    },
    resetUser: () => {
        set({ user: null });
    }
}));