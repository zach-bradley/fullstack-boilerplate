import { defineStore } from 'pinia';
import { authApi, User, AuthResponse } from '../services/auth/auth.api';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  loading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    accessToken: localStorage.getItem('accessToken'),
    refreshToken: localStorage.getItem('refreshToken'),
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    currentUser: (state) => state.user,
  },

  actions: {
    setTokens(access: string, refresh: string) {
      this.accessToken = access;
      this.refreshToken = refresh;
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
    },

    clearTokens() {
      this.accessToken = null;
      this.refreshToken = null;
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    },

    async register(credentials: { email: string; first_name: string; last_name: string; password: string; password2: string }) {
      this.loading = true;
      this.error = null;
      try {
        const response = await authApi.register(credentials);
        this.setTokens(response.access, response.refresh);
        this.user = response.user;
        return response;
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Registration failed';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async login(credentials: { email: string; password: string }) {
      this.loading = true;
      this.error = null;
      try {
        const response = await authApi.login(credentials);
        this.setTokens(response.access, response.refresh);
        this.user = response.user;
        return response;
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Login failed';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async logout() {
      this.clearTokens();
      this.user = null;
    },

    async refreshAccessToken() {
      if (!this.refreshToken) {
        throw new Error('No refresh token available');
      }
      try {
        const response = await authApi.refreshToken(this.refreshToken);
        this.accessToken = response.access;
        localStorage.setItem('accessToken', response.access);
        return response.access;
      } catch (error) {
        this.clearTokens();
        throw error;
      }
    },

    async fetchProfile() {
      try {
        const user = await authApi.getProfile();
        this.user = user;
        return user;
      } catch (error) {
        this.user = null;
        throw error;
      }
    },
  },
}); 