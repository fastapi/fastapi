# dialects/__init__.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

__all__ = (
    "firebird",
    "mssql",
    "mysql",
    "oracle",
    "postgresql",
    "sqlite",
    "sybase",
)


from .. import util


def _auto_fn(name):
    """default dialect importer.

    plugs into the :class:`.PluginLoader`
    as a first-hit system.

    """
    if "." in name:
        dialect, driver = name.split(".")
    else:
        dialect = name
        driver = "base"

    try:
        if dialect == "firebird":
            try:
                module = __import__("sqlalchemy_firebird")
            except ImportError:
                module = __import__("sqlalchemy.dialects.firebird").dialects
                module = getattr(module, dialect)
        elif dialect == "sybase":
            try:
                module = __import__("sqlalchemy_sybase")
            except ImportError:
                module = __import__("sqlalchemy.dialects.sybase").dialects
                module = getattr(module, dialect)
        elif dialect == "mariadb":
            # it's "OK" for us to hardcode here since _auto_fn is already
            # hardcoded.   if mysql / mariadb etc were third party dialects
            # they would just publish all the entrypoints, which would actually
            # look much nicer.
            module = __import__(
                "sqlalchemy.dialects.mysql.mariadb"
            ).dialects.mysql.mariadb
            return module.loader(driver)
        else:
            module = __import__("sqlalchemy.dialects.%s" % (dialect,)).dialects
            module = getattr(module, dialect)
    except ImportError:
        return None

    if hasattr(module, driver):
        module = getattr(module, driver)
        return lambda: module.dialect
    else:
        return None


registry = util.PluginLoader("sqlalchemy.dialects", auto_fn=_auto_fn)

plugins = util.PluginLoader("sqlalchemy.plugins")
