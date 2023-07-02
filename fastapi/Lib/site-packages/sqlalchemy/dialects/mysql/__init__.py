# mysql/__init__.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

from . import base  # noqa
from . import cymysql  # noqa
from . import mariadbconnector  # noqa
from . import mysqlconnector  # noqa
from . import mysqldb  # noqa
from . import oursql  # noqa
from . import pymysql  # noqa
from . import pyodbc  # noqa
from .base import BIGINT
from .base import BINARY
from .base import BIT
from .base import BLOB
from .base import BOOLEAN
from .base import CHAR
from .base import DATE
from .base import DATETIME
from .base import DECIMAL
from .base import DOUBLE
from .base import ENUM
from .base import FLOAT
from .base import INTEGER
from .base import JSON
from .base import LONGBLOB
from .base import LONGTEXT
from .base import MEDIUMBLOB
from .base import MEDIUMINT
from .base import MEDIUMTEXT
from .base import NCHAR
from .base import NUMERIC
from .base import NVARCHAR
from .base import REAL
from .base import SET
from .base import SMALLINT
from .base import TEXT
from .base import TIME
from .base import TIMESTAMP
from .base import TINYBLOB
from .base import TINYINT
from .base import TINYTEXT
from .base import VARBINARY
from .base import VARCHAR
from .base import YEAR
from .dml import Insert
from .dml import insert
from .expression import match
from ...util import compat

if compat.py3k:
    from . import aiomysql  # noqa
    from . import asyncmy  # noqa

# default dialect
base.dialect = dialect = mysqldb.dialect

__all__ = (
    "BIGINT",
    "BINARY",
    "BIT",
    "BLOB",
    "BOOLEAN",
    "CHAR",
    "DATE",
    "DATETIME",
    "DECIMAL",
    "DOUBLE",
    "ENUM",
    "DECIMAL",
    "FLOAT",
    "INTEGER",
    "INTEGER",
    "JSON",
    "LONGBLOB",
    "LONGTEXT",
    "MEDIUMBLOB",
    "MEDIUMINT",
    "MEDIUMTEXT",
    "NCHAR",
    "NVARCHAR",
    "NUMERIC",
    "SET",
    "SMALLINT",
    "REAL",
    "TEXT",
    "TIME",
    "TIMESTAMP",
    "TINYBLOB",
    "TINYINT",
    "TINYTEXT",
    "VARBINARY",
    "VARCHAR",
    "YEAR",
    "dialect",
    "insert",
    "Insert",
    "match",
)
