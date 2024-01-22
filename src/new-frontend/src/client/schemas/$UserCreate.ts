/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserCreate = {
    properties: {
        email: {
    type: 'string',
    isRequired: true,
    format: 'email',
},
        is_active: {
    type: 'boolean',
},
        is_superuser: {
    type: 'boolean',
},
        full_name: {
    type: 'string',
},
        password: {
    type: 'string',
    isRequired: true,
},
    },
} as const;
