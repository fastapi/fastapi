/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Body_login_login_access_token = {
    properties: {
        grant_type: {
    type: 'any-of',
    contains: [{
    type: 'string',
    pattern: 'password',
}, {
    type: 'null',
}],
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
    type: 'any-of',
    contains: [{
    type: 'string',
}, {
    type: 'null',
}],
},
        client_secret: {
    type: 'any-of',
    contains: [{
    type: 'string',
}, {
    type: 'null',
}],
},
    },
} as const;
