# databases/__init__.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""Include imports from the sqlalchemy.dialects package for backwards
compatibility with pre 0.6 versions.

"""
from ..dialects.firebird import base as firebird
from ..dialects.mssql import base as mssql
from ..dialects.mysql import base as mysql
from ..dialects.oracle import base as oracle
from ..dialects.postgresql import base as postgresql
from ..dialects.sqlite import base as sqlite
from ..dialects.sybase import base as sybase
from ..util import warn_deprecated_20

postgres = postgresql


__all__ = (
    "firebird",
    "mssql",
    "mysql",
    "postgresql",
    "sqlite",
    "oracle",
    "sybase",
)


warn_deprecated_20(
    "The `database` package is deprecated and will be removed in v2.0 "
    "of sqlalchemy. Use the `dialects` package instead."
)
