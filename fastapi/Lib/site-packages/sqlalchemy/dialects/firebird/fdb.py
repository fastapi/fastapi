# firebird/fdb.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""
.. dialect:: firebird+fdb
    :name: fdb
    :dbapi: pyodbc
    :connectstring: firebird+fdb://user:password@host:port/path/to/db[?key=value&key=value...]
    :url: https://pypi.org/project/fdb/

    fdb is a kinterbasdb compatible DBAPI for Firebird.

    .. versionchanged:: 0.9 - The fdb dialect is now the default dialect
       under the ``firebird://`` URL space, as ``fdb`` is now the official
       Python driver for Firebird.

Arguments
----------

The ``fdb`` dialect is based on the
:mod:`sqlalchemy.dialects.firebird.kinterbasdb` dialect, however does not
accept every argument that Kinterbasdb does.

* ``enable_rowcount`` - True by default, setting this to False disables
  the usage of "cursor.rowcount" with the
  Kinterbasdb dialect, which SQLAlchemy ordinarily calls upon automatically
  after any UPDATE or DELETE statement.   When disabled, SQLAlchemy's
  CursorResult will return -1 for result.rowcount.   The rationale here is
  that Kinterbasdb requires a second round trip to the database when
  .rowcount is called -  since SQLA's resultproxy automatically closes
  the cursor after a non-result-returning statement, rowcount must be
  called, if at all, before the result object is returned.   Additionally,
  cursor.rowcount may not return correct results with older versions
  of Firebird, and setting this flag to False will also cause the
  SQLAlchemy ORM to ignore its usage. The behavior can also be controlled on a
  per-execution basis using the ``enable_rowcount`` option with
  :meth:`_engine.Connection.execution_options`::

      conn = engine.connect().execution_options(enable_rowcount=True)
      r = conn.execute(stmt)
      print(r.rowcount)

* ``retaining`` - False by default.   Setting this to True will pass the
  ``retaining=True`` keyword argument to the ``.commit()`` and ``.rollback()``
  methods of the DBAPI connection, which can improve performance in some
  situations, but apparently with significant caveats.
  Please read the fdb and/or kinterbasdb DBAPI documentation in order to
  understand the implications of this flag.

  .. versionchanged:: 0.9.0 - the ``retaining`` flag defaults to ``False``.
     In 0.8 it defaulted to ``True``.

  .. seealso::

    https://pythonhosted.org/fdb/usage-guide.html#retaining-transactions
    - information on the "retaining" flag.

"""  # noqa

from ... import util
from .kinterbasdb import FBDialect_kinterbasdb


class FBDialect_fdb(FBDialect_kinterbasdb):
    supports_statement_cache = True

    def __init__(self, enable_rowcount=True, retaining=False, **kwargs):
        super(FBDialect_fdb, self).__init__(
            enable_rowcount=enable_rowcount, retaining=retaining, **kwargs
        )

    @classmethod
    def dbapi(cls):
        return __import__("fdb")

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user")
        if opts.get("port"):
            opts["host"] = "%s/%s" % (opts["host"], opts["port"])
            del opts["port"]
        opts.update(url.query)

        util.coerce_kw_type(opts, "type_conv", int)

        return ([], opts)

    def _get_server_version_info(self, connection):
        """Get the version of the Firebird server used by a connection.

        Returns a tuple of (`major`, `minor`, `build`), three integers
        representing the version of the attached server.
        """

        # This is the simpler approach (the other uses the services api),
        # that for backward compatibility reasons returns a string like
        #   LI-V6.3.3.12981 Firebird 2.0
        # where the first version is a fake one resembling the old
        # Interbase signature.

        isc_info_firebird_version = 103
        fbconn = connection.connection

        version = fbconn.db_info(isc_info_firebird_version)

        return self._parse_version_info(version)


dialect = FBDialect_fdb
