/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UsersOut = {
    properties: {
        data: {
    type: 'array',
    contains: {
        type: 'UserOut',
    },
    isRequired: true,
},
        count: {
    type: 'number',
    isRequired: true,
},
    },
} as const;
