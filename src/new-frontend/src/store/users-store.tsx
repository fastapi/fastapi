import { create } from "zustand";
import { UserCreate, UserOut, UsersService } from "../client";

interface UsersStore {
    users: UserOut[];
    getUsers: () => Promise<void>;
    addUser: (user: UserCreate) => Promise<void>;
    deleteUser: (id: number) => Promise<void>;
}

export const useUsersStore = create<UsersStore>((set) => ({
    users: [],
    getUsers: async () => {
        const usersResponse = await UsersService.readUsers({ skip: 0, limit: 10 });
        set({ users: usersResponse });
    },
    addUser: async (user: UserCreate) => {
        const userResponse = await UsersService.createUser({ requestBody: user });
        set((state) => ({ users: [...state.users, userResponse] }));
    },
    deleteUser: async (id: number) => {
        await UsersService.deleteUser({ userId: id });
        set((state) => ({ users: state.users.filter((user) => user.id !== id) }));
    }
}))