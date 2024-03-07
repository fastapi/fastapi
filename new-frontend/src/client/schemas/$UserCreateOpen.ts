/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserCreateOpen = {
    properties: {
        email: {
    type: 'string',
    isRequired: true,
},
        password: {
    type: 'string',
    isRequired: true,
},
        full_name: {
    type: 'any-of',
    contains: [{
    type: 'string',
}, {
    type: 'null',
}],
},
    },
} as const;
