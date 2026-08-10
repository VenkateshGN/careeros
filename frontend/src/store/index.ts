import { create } from 'zustand';

interface UserState {
    user: null | { id: string, name: string, role: string, email: string };
    setUser: (user: any) => void;
    logout: () => void;
}

export const useUserStore = create<UserState>((set: any) => ({
    user: null, // start explicitly logged out
    setUser: (user: any) => set({ user }),
    logout: () => set({ user: null }),
}));
