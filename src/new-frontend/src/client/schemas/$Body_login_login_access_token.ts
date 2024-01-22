/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Body_login_login_access_token = {
    properties: {
        grant_type: {
    type: 'string',
    pattern: 'password',
},
        username: {
    type: 'string',
    isRequired: true,
},
        password: {
    type: 'string',
    isRequired: true,
},
        scope: {
    type: 'string',
},
        client_id: {
    type: 'string',
},
        client_secret: {
    type: 'string',
},
    },
} as const;
