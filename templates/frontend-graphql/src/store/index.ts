import { defineStore } from 'pinia';
import { User } from '../services/users/user.model';
import { authApi } from '../services/auth/auth.api';
import { userApi } from '@/services/users/user.api';
import { useAuthStore } from './auth.store';

export const useMainStore = defineStore('main', {
    state: () => ({
        isLoading: false as Boolean,
        error: null as string | null,
        authStore: useAuthStore()
    }),

    getters: {
        isAuthenticated: (state) => state.authStore.isAuthenticated,
        currentLocation: (state) => state.locationStore.currentLocation,
        user: (state) => state.authStore.user
    },

    actions: {
        async initializeAuth() {
            try {
                const { valid, user } = await authApi.validateToken();
                if (valid && user) {
                    this.setUser(user);
                    this.setAuth(true);
                } else {
                    this.logout();
                }
            } catch (error) {
                this.logout();
            }
        },

        setAuth(value: boolean) {
            this.authStore.setAuthState(value, this.user);
        },

        setUser(user: User | null) {
            this.user = user;
            if (user) {
                this.authStore.setAuthState(true, user);
            }
        },

        setLoading(value: boolean) {
            this.isLoading = value;
        },

        setError(error: string | null) {
            this.error = error;
        },
        
        async logout() {
            await this.authStore.logout();
            this.setAuth(false);
            this.setUser(null);
            this.setError(null);
        }
    }
});
