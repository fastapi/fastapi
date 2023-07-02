# sqlite/__init__.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

from . import base  # noqa
from . import pysqlcipher  # noqa
from . import pysqlite  # noqa
from .base import BLOB
from .base import BOOLEAN
from .base import CHAR
from .base import DATE
from .base import DATETIME
from .base import DECIMAL
from .base import FLOAT
from .base import INTEGER
from .base import JSON
from .base import NUMERIC
from .base import REAL
from .base import SMALLINT
from .base import TEXT
from .base import TIME
from .base import TIMESTAMP
from .base import VARCHAR
from .dml import Insert
from .dml import insert
from ...util import compat

if compat.py3k:
    from . import aiosqlite  # noqa

# default dialect
base.dialect = dialect = pysqlite.dialect


__all__ = (
    "BLOB",
    "BOOLEAN",
    "CHAR",
    "DATE",
    "DATETIME",
    "DECIMAL",
    "FLOAT",
    "INTEGER",
    "JSON",
    "NUMERIC",
    "SMALLINT",
    "TEXT",
    "TIME",
    "TIMESTAMP",
    "VARCHAR",
    "REAL",
    "Insert",
    "insert",
    "dialect",
)
