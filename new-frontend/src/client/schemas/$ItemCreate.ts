/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ItemCreate = {
    properties: {
        title: {
    type: 'string',
    isRequired: true,
},
        description: {
    type: 'any-of',
    contains: [{
    type: 'string',
}, {
    type: 'null',
}],
},
    },
} as const;
