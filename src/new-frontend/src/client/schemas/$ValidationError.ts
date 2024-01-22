/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ValidationError = {
    properties: {
        loc: {
    type: 'array',
    contains: {
    type: 'any-of',
    contains: [{
    type: 'string',
}, {
    type: 'number',
}],
},
    isRequired: true,
},
        msg: {
    type: 'string',
    isRequired: true,
},
        type: {
    type: 'string',
    isRequired: true,
},
    },
} as const;
