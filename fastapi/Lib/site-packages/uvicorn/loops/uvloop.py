import asyncio

import uvloop


def uvloop_setup(use_subprocess: bool = False) -> None:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
