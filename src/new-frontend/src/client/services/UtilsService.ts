/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Msg } from '../models/Msg';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UtilsService {

    /**
     * Test Celery
     * Test Celery worker.
     * @returns Msg Successful Response
     * @throws ApiError
     */
    public static testCelery({
requestBody,
}: {
requestBody: Msg,
}): CancelablePromise<Msg> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/utils/test-celery/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Test Email
     * Test emails.
     * @returns Msg Successful Response
     * @throws ApiError
     */
    public static testEmail({
emailTo,
}: {
emailTo: string,
}): CancelablePromise<Msg> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/utils/test-email/',
            query: {
                'email_to': emailTo,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
