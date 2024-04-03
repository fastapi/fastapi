import type { ApiResult } from './ApiResult';

export type TResult = 'body' | 'raw';

export type TApiResponse<T extends TResult, TData> =
  Exclude<T, 'raw'> extends never
    ? ApiResult<TData>
    : ApiResult<TData>['body'];

export type TConfig<T extends TResult> = {
  _result?: T;
};