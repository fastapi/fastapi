import logging
import warnings
from typing import Annotated, Any, Callable

from annotated_doc import Doc
from starlette.background import BackgroundTask, BackgroundTasks as StarletteBackgroundTasks
from typing_extensions import ParamSpec

P = ParamSpec("P")

logger = logging.getLogger("fastapi.background")


class BackgroundTaskError(Exception):
    """Exception raised when multiple background tasks fail.

    Attributes:
        errors: List of (task, exception) tuples for each failed task.
                Note: Holding references to tasks may keep their args/kwargs
                in memory until this exception is garbage collected.
    """

    def __init__(self, errors: list[tuple[BackgroundTask, BaseException]]):
        self.errors = errors
        task_count = len(errors)
        super().__init__(f"{task_count} background task(s) failed")


class BackgroundTasks(StarletteBackgroundTasks):
    """
    A collection of background tasks that will be called after a response has been
    sent to the client.

    Read more about it in the
    [FastAPI docs for Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).

    ## Example

    ```python
    from fastapi import BackgroundTasks, FastAPI

    app = FastAPI()


    def write_notification(email: str, message=""):
        with open("log.txt", mode="w") as email_file:
            content = f"notification for {email}: {message}"
            email_file.write(content)


    @app.post("/send-notification/{email}")
    async def send_notification(email: str, background_tasks: BackgroundTasks):
        background_tasks.add_task(write_notification, email, message="some notification")
        return {"message": "Notification sent in the background"}
    ```
    """

    def __init__(self, tasks: list[BackgroundTask] | None = None):
        super().__init__(tasks)
        self._executed = False

    def add_task(
        self,
        func: Annotated[
            Callable[P, Any],
            Doc(
                """
                The function to call after the response is sent.

                It can be a regular `def` function or an `async def` function.
                """
            ),
        ],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        """
        Add a function to be called in the background after the response is sent.

        Read more about it in the
        [FastAPI docs for Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).
        """
        if self._executed:
            warnings.warn(
                "Background task added after tasks have already been executed. "
                "This task will not run. This commonly happens when adding tasks "
                "after a 'yield' in a dependency. Consider adding tasks before "
                "the yield, or use a different approach for cleanup tasks.",
                UserWarning,
                stacklevel=2,
            )
            return
        return super().add_task(func, *args, **kwargs)

    def _get_task_name(self, task: BackgroundTask) -> str:
        """Safely get a task name for logging."""
        try:
            name = getattr(task.func, "__name__", None)
            if name is not None:
                return name
            return repr(task.func)
        except Exception:
            return "<unknown>"

    async def __call__(self) -> None:
        """
        Execute all background tasks.

        Unlike Starlette's implementation, this continues executing remaining
        tasks even if some tasks fail, ensuring all tasks get a chance to run.
        Errors are collected and logged.

        For backward compatibility:
        - If only one task fails, the original exception is re-raised
        - If multiple tasks fail, a BackgroundTaskError is raised with all errors
        """
        # Fix #8: Snapshot tasks to prevent mutation during iteration
        tasks_snapshot = list(self.tasks)

        # Fix #7: Set _executed after snapshot, so it reflects actual execution attempt
        self._executed = True

        errors: list[tuple[BackgroundTask, BaseException]] = []

        for task in tasks_snapshot:
            try:
                await task()
            except BaseException as exc:
                # Fix #1: Catch BaseException but re-raise critical exceptions
                # that should not be suppressed
                if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                    raise

                # Fix #2 & #10: Safe logging that won't break the loop
                # Use %-style formatting for lazy evaluation
                try:
                    if logger.isEnabledFor(logging.ERROR):
                        task_name = self._get_task_name(task)
                        logger.exception(
                            "Background task %s failed", task_name
                        )
                except Exception:
                    # Never let logging failures break task execution
                    pass

                # Fix #6: Wrap in try/except to handle MemoryError etc.
                try:
                    errors.append((task, exc))
                except BaseException:
                    # If we can't even store the error (e.g., MemoryError),
                    # just continue to give remaining tasks a chance
                    pass

        # Handle errors with backward compatibility
        if len(errors) == 1:
            # Fix #5: Single error - re-raise with proper context
            # Using 'from' preserves the chain and adds context
            original_exc = errors[0][1]
            raise original_exc from original_exc
        elif len(errors) > 1:
            # Multiple errors: raise aggregate exception
            raise BackgroundTaskError(errors)
