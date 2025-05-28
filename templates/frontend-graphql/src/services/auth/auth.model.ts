import { authApi } from './auth.api';

export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegisterRequest extends LoginRequest {
    firstName: string;
    lastName: string;
}

export interface AuthResponse {
    accessToken: string;
    refreshToken: string;
}

export const model = {
    api: authApi
};