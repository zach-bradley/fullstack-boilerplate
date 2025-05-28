import { User, UserInput, UserUpdateInput } from './user.model';
import { mutationBase } from '../../graphql/mutation';
import { queryBase } from '../../graphql/query';
import { authApi } from '../auth/auth.api';

export class UserApi {
    private baseUrl = "/graphql";

    private async handleResponse(response: Response) {
        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }
        return response.json();
    }

    getHeaders() {
        return authApi.getHeaders();
    }

    async getCurrentUser(token: String): Promise<User> {
        const meQuery = queryBase(
            "me",
            "me",
            ["id", "email", "firstName", "lastName"],
            {token: {type:"String!",value:token}}
        );
        console.log(meQuery)
        const response = await fetch(`${this.baseUrl}`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({
                query: meQuery,
                variables: {token:token}
            })
        });
        const data = await this.handleResponse(response);
        return data.data.me;
    }

    async updateUser(userId: string, userData: UserUpdateInput): Promise<User> {
        const updateUserMutation = mutationBase(
            "updateUser",
            ["id", "email", "firstName", "lastName"],
            { 
                userId: { type: "ID!", value: userId },
                userData: { type: "UserUpdateInput!", value: userData }
            },
            "updateUser"
        );
        const response = await fetch(`${this.baseUrl}`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({
                query: updateUserMutation,
                variables: { userId, userData }
            })
        });
        const data = await this.handleResponse(response);
        return data.data.updateUser;
    }
}

export const userApi = new UserApi();
