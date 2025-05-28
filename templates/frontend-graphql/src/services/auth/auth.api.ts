import { LoginRequest, RegisterRequest, AuthResponse } from './auth.model';
import { User } from '../users/user.model';

export class AuthApi {
    private baseUrl = "http://localhost:8000/api/auth";
    private token: string | null = null;

    private async handleResponse(response: Response) {
        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }
        return response.json();
    }

    setToken(token: string) {
        this.token = token;
        localStorage.setItem('accessToken', token);
    }

    getToken(): string | null {
        if (!this.token) {
            this.token = localStorage.getItem('accessToken');
        }
        return this.token;
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('accessToken');
    }

    getHeaders() {
        const headers: Record<string, string> = {
            'Content-Type': 'application/json'
        };
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    async login(request: LoginRequest): Promise<AuthResponse> {
        const response = await fetch(`${this.baseUrl}/login/`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({
                email: request.email,
                password: request.password
            })
        });
        const data = await this.handleResponse(response);
        if (data.access) {
            this.setToken(data.access);
            // Fetch user data after successful login
            const user = await this.getCurrentUser();
            return { ...data, user };
        }
        return data;
    }

    async register(request: RegisterRequest): Promise<AuthResponse> {
        const response = await fetch(`${this.baseUrl}/register/`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({
                email: request.email,
                password: request.password,
                password2: request.password,
                first_name: request.firstName,
                last_name: request.lastName
            })
        });
        const data = await this.handleResponse(response);
        if (data.access) {
            this.setToken(data.access);
            // Fetch user data after successful registration
            const user = await this.getCurrentUser();
            return { ...data, user };
        }
        return data;
    }

    async getCurrentUser(): Promise<User> {
        const response = await fetch(`${this.baseUrl}/profile/`, {
            method: 'GET',
            headers: this.getHeaders()
        });
        return this.handleResponse(response);
    }

    async refreshToken(): Promise<{ access: string }> {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
            throw new Error('No refresh token available');
        }
        const response = await fetch(`${this.baseUrl}/token/refresh/`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({
                refresh: refreshToken
            })
        });
        const data = await this.handleResponse(response);
        if (data.access) {
            this.setToken(data.access);
        }
        return data;
    }

    async logout(): Promise<void> {
        this.clearToken();
        localStorage.removeItem('refreshToken');
    }
}

export const authApi = new AuthApi();
