import { create } from "zustand";
import { UserOut, UsersService } from "../client";

interface UserStore {
    user: UserOut | null;
    getUser: () => Promise<void>;
    resetUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
    user: null,
    getUser: async () => {
        const user = await UsersService.readUserMe();
        set({ user });
    },
    resetUser: () => {
        set({ user: null });
    }
}));