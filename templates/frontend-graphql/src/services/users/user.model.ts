export interface User {
    id: number;
    email: string;
    firstName: string;
    lastName: string;
}

export interface UserInput {
    email: string;
    password: string;
    firstName?: string;
    lastName?: string;
}

export interface UserUpdateInput {
    firstName?: string;
    lastName?: string;
    email?: string;
}

