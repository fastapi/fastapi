/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export class CancelError extends Error {

    constructor(message: string) {
        super(message);
        this.name = 'CancelError';
    }

    public get isCancelled(): boolean {
        return true;
    }
}

export interface OnCancel {
    readonly isResolved: boolean;
    readonly isRejected: boolean;
    readonly isCancelled: boolean;

    (cancelHandler: () => void): void;
}

export class CancelablePromise<T> implements Promise<T> {
    #isResolved: boolean;
    #isRejected: boolean;
    #isCancelled: boolean;
    readonly #cancelHandlers: (() => void)[];
    readonly #promise: Promise<T>;
    #resolve?: (value: T | PromiseLike<T>) => void;
    #reject?: (reason?: any) => void;

    constructor(
        executor: (
            resolve: (value: T | PromiseLike<T>) => void,
            reject: (reason?: any) => void,
            onCancel: OnCancel
        ) => void
    ) {
        this.#isResolved = false;
        this.#isRejected = false;
        this.#isCancelled = false;
        this.#cancelHandlers = [];
        this.#promise = new Promise<T>((resolve, reject) => {
            this.#resolve = resolve;
            this.#reject = reject;

            const onResolve = (value: T | PromiseLike<T>): void => {
                if (this.#isResolved || this.#isRejected || this.#isCancelled) {
                    return;
                }
                this.#isResolved = true;
                this.#resolve?.(value);
            };

            const onReject = (reason?: any): void => {
                if (this.#isResolved || this.#isRejected || this.#isCancelled) {
                    return;
                }
                this.#isRejected = true;
                this.#reject?.(reason);
            };

            const onCancel = (cancelHandler: () => void): void => {
                if (this.#isResolved || this.#isRejected || this.#isCancelled) {
                    return;
                }
                this.#cancelHandlers.push(cancelHandler);
            };

            Object.defineProperty(onCancel, 'isResolved', {
                get: (): boolean => this.#isResolved,
            });

            Object.defineProperty(onCancel, 'isRejected', {
                get: (): boolean => this.#isRejected,
            });

            Object.defineProperty(onCancel, 'isCancelled', {
                get: (): boolean => this.#isCancelled,
            });

            return executor(onResolve, onReject, onCancel as OnCancel);
        });
    }

     get [Symbol.toStringTag]() {
            return "Cancellable Promise";
     }

    public then<TResult1 = T, TResult2 = never>(
        onFulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | null,
        onRejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | null
    ): Promise<TResult1 | TResult2> {
        return this.#promise.then(onFulfilled, onRejected);
    }

    public catch<TResult = never>(
        onRejected?: ((reason: any) => TResult | PromiseLike<TResult>) | null
    ): Promise<T | TResult> {
        return this.#promise.catch(onRejected);
    }

    public finally(onFinally?: (() => void) | null): Promise<T> {
        return this.#promise.finally(onFinally);
    }

    public cancel(): void {
        if (this.#isResolved || this.#isRejected || this.#isCancelled) {
            return;
        }
        this.#isCancelled = true;
        if (this.#cancelHandlers.length) {
            try {
                for (const cancelHandler of this.#cancelHandlers) {
                    cancelHandler();
                }
            } catch (error) {
                console.warn('Cancellation threw an error', error);
                return;
            }
        }
        this.#cancelHandlers.length = 0;
        this.#reject?.(new CancelError('Request aborted'));
    }

    public get isCancelled(): boolean {
        return this.#isCancelled;
    }
}
