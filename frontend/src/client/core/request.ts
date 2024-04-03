import axios from 'axios';
import type { AxiosError, AxiosRequestConfig, AxiosResponse, AxiosInstance } from 'axios';

import { ApiError } from './ApiError';
import type { ApiRequestOptions } from './ApiRequestOptions';
import type { ApiResult } from './ApiResult';
import { CancelablePromise } from './CancelablePromise';
import type { OnCancel } from './CancelablePromise';
import type { OpenAPIConfig } from './OpenAPI';

export const isString = (value: unknown): value is string => {
	return typeof value === 'string';
};

export const isStringWithValue = (value: unknown): value is string => {
	return isString(value) && value !== '';
};

export const isBlob = (value: any): value is Blob => {
	return value instanceof Blob;
};

export const isFormData = (value: unknown): value is FormData => {
	return value instanceof FormData;
};

export const isSuccess = (status: number): boolean => {
	return status >= 200 && status < 300;
};

export const base64 = (str: string): string => {
	try {
		return btoa(str);
	} catch (err) {
		// @ts-ignore
		return Buffer.from(str).toString('base64');
	}
};

export const getQueryString = (params: Record<string, unknown>): string => {
	const qs: string[] = [];

	const append = (key: string, value: unknown) => {
		qs.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`);
	};

	const encodePair = (key: string, value: unknown) => {
		if (value === undefined || value === null) {
			return;
		}

		if (Array.isArray(value)) {
			value.forEach(v => encodePair(key, v));
		} else if (typeof value === 'object') {
			Object.entries(value).forEach(([k, v]) => encodePair(`${key}[${k}]`, v));
		} else {
			append(key, value);
		}
	};

	Object.entries(params).forEach(([key, value]) => encodePair(key, value));

	return qs.length ? `?${qs.join('&')}` : '';
};

const getUrl = (config: OpenAPIConfig, options: ApiRequestOptions): string => {
	const encoder = config.ENCODE_PATH || encodeURI;

	const path = options.url
		.replace('{api-version}', config.VERSION)
		.replace(/{(.*?)}/g, (substring: string, group: string) => {
			if (options.path?.hasOwnProperty(group)) {
				return encoder(String(options.path[group]));
			}
			return substring;
		});

	const url = config.BASE + path;
	return options.query ? url + getQueryString(options.query) : url;
};

export const getFormData = (options: ApiRequestOptions): FormData | undefined => {
	if (options.formData) {
		const formData = new FormData();

		const process = (key: string, value: unknown) => {
			if (isString(value) || isBlob(value)) {
				formData.append(key, value);
			} else {
				formData.append(key, JSON.stringify(value));
			}
		};

		Object.entries(options.formData)
			.filter(([, value]) => value !== undefined && value !== null)
			.forEach(([key, value]) => {
				if (Array.isArray(value)) {
					value.forEach(v => process(key, v));
				} else {
					process(key, value);
				}
			});

		return formData;
	}
	return undefined;
};

type Resolver<T> = (options: ApiRequestOptions) => Promise<T>;

export const resolve = async <T>(options: ApiRequestOptions, resolver?: T | Resolver<T>): Promise<T | undefined> => {
	if (typeof resolver === 'function') {
		return (resolver as Resolver<T>)(options);
	}
	return resolver;
};

export const getHeaders = async (config: OpenAPIConfig, options: ApiRequestOptions): Promise<Record<string, string>> => {
	const [token, username, password, additionalHeaders] = await Promise.all([
		resolve(options, config.TOKEN),
		resolve(options, config.USERNAME),
		resolve(options, config.PASSWORD),
		resolve(options, config.HEADERS),
	]);

	const headers = Object.entries({
		Accept: 'application/json',
		...additionalHeaders,
		...options.headers,
	})
	.filter(([, value]) => value !== undefined && value !== null)
	.reduce((headers, [key, value]) => ({
		...headers,
		[key]: String(value),
	}), {} as Record<string, string>);

	if (isStringWithValue(token)) {
		headers['Authorization'] = `Bearer ${token}`;
	}

	if (isStringWithValue(username) && isStringWithValue(password)) {
		const credentials = base64(`${username}:${password}`);
		headers['Authorization'] = `Basic ${credentials}`;
	}

	if (options.body !== undefined) {
		if (options.mediaType) {
			headers['Content-Type'] = options.mediaType;
		} else if (isBlob(options.body)) {
			headers['Content-Type'] = options.body.type || 'application/octet-stream';
		} else if (isString(options.body)) {
			headers['Content-Type'] = 'text/plain';
		} else if (!isFormData(options.body)) {
			headers['Content-Type'] = 'application/json';
		}
	} else if (options.formData !== undefined) {
		if (options.mediaType) {
			headers['Content-Type'] = options.mediaType;
		}
	}

	return headers;
};

export const getRequestBody = (options: ApiRequestOptions): unknown => {
	if (options.body) {
		return options.body;
	}
	return undefined;
};

export const sendRequest = async <T>(
	config: OpenAPIConfig,
	options: ApiRequestOptions,
	url: string,
	body: unknown,
	formData: FormData | undefined,
	headers: Record<string, string>,
	onCancel: OnCancel,
	axiosClient: AxiosInstance
): Promise<AxiosResponse<T>> => {
	const controller = new AbortController();

	let requestConfig: AxiosRequestConfig = {
		data: body ?? formData,
		headers,
		method: options.method,
		signal: controller.signal,
		url,
		withCredentials: config.WITH_CREDENTIALS,
	};

	onCancel(() => controller.abort());

	for (const fn of config.interceptors.request._fns) {
		requestConfig = await fn(requestConfig)
	}

	try {
		return await axiosClient.request(requestConfig);
	} catch (error) {
		const axiosError = error as AxiosError<T>;
		if (axiosError.response) {
			return axiosError.response;
		}
		throw error;
	}
};

export const getResponseHeader = (response: AxiosResponse<unknown>, responseHeader?: string): string | undefined => {
	if (responseHeader) {
		const content = response.headers[responseHeader];
		if (isString(content)) {
			return content;
		}
	}
	return undefined;
};

export const getResponseBody = (response: AxiosResponse<unknown>): unknown => {
	if (response.status !== 204) {
		return response.data;
	}
	return undefined;
};

export const catchErrorCodes = (options: ApiRequestOptions, result: ApiResult): void => {
	const errors: Record<number, string> = {
		400: 'Bad Request',
		401: 'Unauthorized',
		402: 'Payment Required',
		403: 'Forbidden',
		404: 'Not Found',
		405: 'Method Not Allowed',
		406: 'Not Acceptable',
		407: 'Proxy Authentication Required',
		408: 'Request Timeout',
		409: 'Conflict',
		410: 'Gone',
		411: 'Length Required',
		412: 'Precondition Failed',
		413: 'Payload Too Large',
		414: 'URI Too Long',
		415: 'Unsupported Media Type',
		416: 'Range Not Satisfiable',
		417: 'Expectation Failed',
		418: 'Im a teapot',
		421: 'Misdirected Request',
		422: 'Unprocessable Content',
		423: 'Locked',
		424: 'Failed Dependency',
		425: 'Too Early',
		426: 'Upgrade Required',
		428: 'Precondition Required',
		429: 'Too Many Requests',
		431: 'Request Header Fields Too Large',
		451: 'Unavailable For Legal Reasons',
		500: 'Internal Server Error',
		501: 'Not Implemented',
		502: 'Bad Gateway',
		503: 'Service Unavailable',
		504: 'Gateway Timeout',
		505: 'HTTP Version Not Supported',
		506: 'Variant Also Negotiates',
		507: 'Insufficient Storage',
		508: 'Loop Detected',
		510: 'Not Extended',
		511: 'Network Authentication Required',
		...options.errors,
	}

	const error = errors[result.status];
	if (error) {
		throw new ApiError(options, result, error);
	}

	if (!result.ok) {
		const errorStatus = result.status ?? 'unknown';
		const errorStatusText = result.statusText ?? 'unknown';
		const errorBody = (() => {
			try {
				return JSON.stringify(result.body, null, 2);
			} catch (e) {
				return undefined;
			}
		})();

		throw new ApiError(options, result,
			`Generic Error: status: ${errorStatus}; status text: ${errorStatusText}; body: ${errorBody}`
		);
	}
};

/**
 * Request method
 * @param config The OpenAPI configuration object
 * @param options The request options from the service
 * @param axiosClient The axios client instance to use
 * @returns CancelablePromise<T>
 * @throws ApiError
 */
export const request = <T>(config: OpenAPIConfig, options: ApiRequestOptions, axiosClient: AxiosInstance = axios): CancelablePromise<T> => {
	return new CancelablePromise(async (resolve, reject, onCancel) => {
		try {
			const url = getUrl(config, options);
			const formData = getFormData(options);
			const body = getRequestBody(options);
			const headers = await getHeaders(config, options);

			if (!onCancel.isCancelled) {
				let response = await sendRequest<T>(config, options, url, body, formData, headers, onCancel, axiosClient);

				for (const fn of config.interceptors.response._fns) {
					response = await fn(response)
				}

				const responseBody = getResponseBody(response);
				const responseHeader = getResponseHeader(response, options.responseHeader);

				const result: ApiResult = {
					url,
					ok: isSuccess(response.status),
					status: response.status,
					statusText: response.statusText,
					body: responseHeader ?? responseBody,
				};

				catchErrorCodes(options, result);

				resolve(result.body);
			}
		} catch (error) {
			reject(error);
		}
	});
};