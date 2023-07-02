# ext/asyncio/exc.py
# Copyright (C) 2020-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

from ... import exc


class AsyncMethodRequired(exc.InvalidRequestError):
    """an API can't be used because its result would not be
    compatible with async"""


class AsyncContextNotStarted(exc.InvalidRequestError):
    """a startable context manager has not been started."""


class AsyncContextAlreadyStarted(exc.InvalidRequestError):
    """a startable context manager is already started."""
