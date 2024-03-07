/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Message } from '../models/Message';
import type { UpdatePassword } from '../models/UpdatePassword';
import type { UserCreate } from '../models/UserCreate';
import type { UserCreateOpen } from '../models/UserCreateOpen';
import type { UserOut } from '../models/UserOut';
import type { UsersOut } from '../models/UsersOut';
import type { UserUpdate } from '../models/UserUpdate';
import type { UserUpdateMe } from '../models/UserUpdateMe';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UsersService {

    /**
     * Read Users
     * Retrieve users.
     * @returns UsersOut Successful Response
     * @throws ApiError
     */
    public static readUsers({
skip,
limit = 100,
}: {
skip?: number,
limit?: number,
}): CancelablePromise<UsersOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/',
            query: {
                'skip': skip,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create User
     * Create new user.
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public static createUser({
requestBody,
}: {
requestBody: UserCreate,
}): CancelablePromise<UserOut> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/users/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read User Me
     * Get current user.
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public static readUserMe(): CancelablePromise<UserOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/me',
        });
    }

    /**
     * Update User Me
     * Update own user.
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public static updateUserMe({
requestBody,
}: {
requestBody: UserUpdateMe,
}): CancelablePromise<UserOut> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/users/me',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Password Me
     * Update own password.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static updatePasswordMe({
requestBody,
}: {
requestBody: UpdatePassword,
}): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/users/me/password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create User Open
     * Create new user without the need to be logged in.
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public static createUserOpen({
requestBody,
}: {
requestBody: UserCreateOpen,
}): CancelablePromise<UserOut> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/users/open',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read User By Id
     * Get a specific user by id.
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public static readUserById({
userId,
}: {
userId: number,
}): CancelablePromise<UserOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User
     * Update a user.
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public static updateUser({
userId,
requestBody,
}: {
userId: number,
requestBody: UserUpdate,
}): CancelablePromise<UserOut> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/users/{user_id}',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete User
     * Delete a user.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static deleteUser({
userId,
}: {
userId: number,
}): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
