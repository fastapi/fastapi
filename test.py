from contextlib import AsyncExitStack


NOSEND = object()


class DependencyAsyncExitStack(AsyncExitStack):

    def __init__(self) -> None:
        super().__init__()
        self.send = NOSEND
    
    async def enter_async_context(self, cm):
        res = await super().enter_async_context(cm)