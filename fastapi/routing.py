import contextlib
import copy
import email.message
import errno
import functools
import inspect
import json
import os
import stat
import threading
import types
import warnings
from collections.abc import (
    AsyncIterator,
    Awaitable,
    Callable,
    Collection,
    Coroutine,
    Generator,
    Iterator,
    Mapping,
    Sequence,
)
from contextlib import (
    AbstractAsyncContextManager,
    AbstractContextManager,
    AsyncExitStack,
    asynccontextmanager,
)

# Note: Restore explicit APIRoute.tags type annotation for type checkers (#15764)
