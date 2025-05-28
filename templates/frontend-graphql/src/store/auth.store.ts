import { defineStore } from 'pinia';
import { User } from '../services/users/user.model';
import { authApi } from '../services/auth/auth.api';

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    isAuthenticated: false,
    user: null
  }),
  
  actions: {
    setAuthState(isAuthenticated: boolean, user: User | null = null) {
      this.isAuthenticated = isAuthenticated;
      this.user = user;
    },
    
    login(user: User) {
      this.isAuthenticated = true;
      this.user = user;
    },
    
    logout() {
      this.isAuthenticated = false;
      this.user = null;
    },
    
    async validateStoredAuth() {
      try {
        const user = await authApi.getCurrentUser();
        this.user = user;
        this.isAuthenticated = true;
        return true;
      } catch (error) {
        console.error('Error validating session:', error);
        this.logout();
        return false;
      }
    },

    async withSessionRefresh<T>(operation: () => Promise<T>): Promise<T> {
      try {
        return await operation();
      } catch (error) {
        if (error.message.includes('session')) {
          await authApi.refreshSession();
          return await operation();
        }
        throw error;
      }
    }
  }
}); 

let lastActivity = Date.now();

function trackActivity() {
  lastActivity = Date.now();
}

async function checkAndRefreshSession() {
  const now = Date.now();
  const timeSinceLastActivity = now - lastActivity;
  
  // Only refresh if user has been active in the last 5 minutes
  if (timeSinceLastActivity < 5 * 60 * 1000) {
    await authApi.refreshSession();
  }
}

// Track user interactions
document.addEventListener('touchstart', trackActivity);
document.addEventListener('click', trackActivity); 