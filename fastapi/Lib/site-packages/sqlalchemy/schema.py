# schema.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""Compatibility namespace for sqlalchemy.sql.schema and related.

"""

from .sql.base import SchemaVisitor  # noqa
from .sql.ddl import _CreateDropBase  # noqa
from .sql.ddl import _DDLCompiles  # noqa
from .sql.ddl import _DropView  # noqa
from .sql.ddl import AddConstraint  # noqa
from .sql.ddl import CreateColumn  # noqa
from .sql.ddl import CreateIndex  # noqa
from .sql.ddl import CreateSchema  # noqa
from .sql.ddl import CreateSequence  # noqa
from .sql.ddl import CreateTable  # noqa
from .sql.ddl import DDL  # noqa
from .sql.ddl import DDLBase  # noqa
from .sql.ddl import DDLElement  # noqa
from .sql.ddl import DropColumnComment  # noqa
from .sql.ddl import DropConstraint  # noqa
from .sql.ddl import DropIndex  # noqa
from .sql.ddl import DropSchema  # noqa
from .sql.ddl import DropSequence  # noqa
from .sql.ddl import DropTable  # noqa
from .sql.ddl import DropTableComment  # noqa
from .sql.ddl import SetColumnComment  # noqa
from .sql.ddl import SetTableComment  # noqa
from .sql.ddl import sort_tables  # noqa
from .sql.ddl import sort_tables_and_constraints  # noqa
from .sql.naming import conv  # noqa
from .sql.schema import _get_table_key  # noqa
from .sql.schema import BLANK_SCHEMA  # noqa
from .sql.schema import CheckConstraint  # noqa
from .sql.schema import Column  # noqa
from .sql.schema import ColumnCollectionConstraint  # noqa
from .sql.schema import ColumnCollectionMixin  # noqa
from .sql.schema import ColumnDefault  # noqa
from .sql.schema import Computed  # noqa
from .sql.schema import Constraint  # noqa
from .sql.schema import DefaultClause  # noqa
from .sql.schema import DefaultGenerator  # noqa
from .sql.schema import FetchedValue  # noqa
from .sql.schema import ForeignKey  # noqa
from .sql.schema import ForeignKeyConstraint  # noqa
from .sql.schema import Identity  # noqa
from .sql.schema import Index  # noqa
from .sql.schema import MetaData  # noqa
from .sql.schema import PrimaryKeyConstraint  # noqa
from .sql.schema import SchemaItem  # noqa
from .sql.schema import Sequence  # noqa
from .sql.schema import Table  # noqa
from .sql.schema import ThreadLocalMetaData  # noqa
from .sql.schema import UniqueConstraint  # noqa
