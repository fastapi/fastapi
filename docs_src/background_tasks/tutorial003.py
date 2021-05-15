import asyncio
import functools
import typing

from fastapi import BackgroundTasks, FastAPI


async def delayed(fn, duration=5):
    print(f"Waiting {duration} seconds")
    await asyncio.sleep(duration)
    return await fn()


class CustomBackgroundTasks(BackgroundTasks):
    def add_task(
        self, func: typing.Callable, *args: typing.Any, **kwargs: typing.Any
    ) -> None:
        super().add_task(delayed, functools.partial(func, *args, **kwargs))


app = FastAPI()

app.dependency_overrides[BackgroundTasks] = CustomBackgroundTasks


async def task():
    print("Running task!")


@app.get("/delayed-background-task")
async def delayed_background_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(task)
