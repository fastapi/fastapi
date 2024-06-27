export class CancelError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "CancelError"
  }

  public get isCancelled(): boolean {
    return true
  }
}

export interface OnCancel {
  readonly isResolved: boolean
  readonly isRejected: boolean
  readonly isCancelled: boolean

  (cancelHandler: () => void): void
}

export class CancelablePromise<T> implements Promise<T> {
  private _isResolved: boolean
  private _isRejected: boolean
  private _isCancelled: boolean
  readonly cancelHandlers: (() => void)[]
  readonly promise: Promise<T>
  private _resolve?: (value: T | PromiseLike<T>) => void
  private _reject?: (reason?: unknown) => void

  constructor(
    executor: (
      resolve: (value: T | PromiseLike<T>) => void,
      reject: (reason?: unknown) => void,
      onCancel: OnCancel,
    ) => void,
  ) {
    this._isResolved = false
    this._isRejected = false
    this._isCancelled = false
    this.cancelHandlers = []
    this.promise = new Promise<T>((resolve, reject) => {
      this._resolve = resolve
      this._reject = reject

      const onResolve = (value: T | PromiseLike<T>): void => {
        if (this._isResolved || this._isRejected || this._isCancelled) {
          return
        }
        this._isResolved = true
        if (this._resolve) this._resolve(value)
      }

      const onReject = (reason?: unknown): void => {
        if (this._isResolved || this._isRejected || this._isCancelled) {
          return
        }
        this._isRejected = true
        if (this._reject) this._reject(reason)
      }

      const onCancel = (cancelHandler: () => void): void => {
        if (this._isResolved || this._isRejected || this._isCancelled) {
          return
        }
        this.cancelHandlers.push(cancelHandler)
      }

      Object.defineProperty(onCancel, "isResolved", {
        get: (): boolean => this._isResolved,
      })

      Object.defineProperty(onCancel, "isRejected", {
        get: (): boolean => this._isRejected,
      })

      Object.defineProperty(onCancel, "isCancelled", {
        get: (): boolean => this._isCancelled,
      })

      return executor(onResolve, onReject, onCancel as OnCancel)
    })
  }

  get [Symbol.toStringTag]() {
    return "Cancellable Promise"
  }

  public then<TResult1 = T, TResult2 = never>(
    onFulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | null,
    onRejected?: ((reason: unknown) => TResult2 | PromiseLike<TResult2>) | null,
  ): Promise<TResult1 | TResult2> {
    return this.promise.then(onFulfilled, onRejected)
  }

  public catch<TResult = never>(
    onRejected?: ((reason: unknown) => TResult | PromiseLike<TResult>) | null,
  ): Promise<T | TResult> {
    return this.promise.catch(onRejected)
  }

  public finally(onFinally?: (() => void) | null): Promise<T> {
    return this.promise.finally(onFinally)
  }

  public cancel(): void {
    if (this._isResolved || this._isRejected || this._isCancelled) {
      return
    }
    this._isCancelled = true
    if (this.cancelHandlers.length) {
      try {
        for (const cancelHandler of this.cancelHandlers) {
          cancelHandler()
        }
      } catch (error) {
        console.warn("Cancellation threw an error", error)
        return
      }
    }
    this.cancelHandlers.length = 0
    if (this._reject) this._reject(new CancelError("Request aborted"))
  }

  public get isCancelled(): boolean {
    return this._isCancelled
  }
}
