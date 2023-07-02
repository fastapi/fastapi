# sqlalchemy/pool/dbapi_proxy.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php


"""DBAPI proxy utility.

Provides transparent connection pooling on top of a Python DBAPI.

This is legacy SQLAlchemy functionality that is not typically used
today.

"""

from .. import util
from ..util import threading
from .impl import QueuePool

proxies = {}


@util.deprecated(
    "1.3",
    "The :func:`.pool.manage` function is deprecated, and will be "
    "removed in a future release.",
)
def manage(module, **params):
    r"""Return a proxy for a DB-API module that automatically
    pools connections.

    Given a DB-API 2.0 module and pool management parameters, returns
    a proxy for the module that will automatically pool connections,
    creating new connection pools for each distinct set of connection
    arguments sent to the decorated module's connect() function.

    :param module: a DB-API 2.0 database module

    :param poolclass: the class used by the pool module to provide
      pooling.  Defaults to :class:`.QueuePool`.

    :param \**params: will be passed through to *poolclass*

    """
    try:
        return proxies[module]
    except KeyError:
        return proxies.setdefault(module, _DBProxy(module, **params))


def clear_managers():
    """Remove all current DB-API 2.0 managers.

    All pools and connections are disposed.
    """

    for manager in proxies.values():
        manager.close()
    proxies.clear()


class _DBProxy(object):

    """Layers connection pooling behavior on top of a standard DB-API module.

    Proxies a DB-API 2.0 connect() call to a connection pool keyed to the
    specific connect parameters. Other functions and attributes are delegated
    to the underlying DB-API module.
    """

    def __init__(self, module, poolclass=QueuePool, **kw):
        """Initializes a new proxy.

        module
          a DB-API 2.0 module

        poolclass
          a Pool class, defaulting to QueuePool

        Other parameters are sent to the Pool object's constructor.

        """

        self.module = module
        self.kw = kw
        self.poolclass = poolclass
        self.pools = {}
        self._create_pool_mutex = threading.Lock()

    def close(self):
        for key in list(self.pools):
            del self.pools[key]

    def __del__(self):
        self.close()

    def __getattr__(self, key):
        return getattr(self.module, key)

    def get_pool(self, *args, **kw):
        key = self._serialize(*args, **kw)
        try:
            return self.pools[key]
        except KeyError:
            with self._create_pool_mutex:
                if key not in self.pools:
                    kw.pop("sa_pool_key", None)
                    pool = self.poolclass(
                        lambda: self.module.connect(*args, **kw), **self.kw
                    )
                    self.pools[key] = pool
                    return pool
                else:
                    return self.pools[key]

    def connect(self, *args, **kw):
        """Activate a connection to the database.

        Connect to the database using this DBProxy's module and the given
        connect arguments.  If the arguments match an existing pool, the
        connection will be returned from the pool's current thread-local
        connection instance, or if there is no thread-local connection
        instance it will be checked out from the set of pooled connections.

        If the pool has no available connections and allows new connections
        to be created, a new database connection will be made.

        """

        return self.get_pool(*args, **kw).connect()

    def dispose(self, *args, **kw):
        """Dispose the pool referenced by the given connect arguments."""

        key = self._serialize(*args, **kw)
        try:
            del self.pools[key]
        except KeyError:
            pass

    def _serialize(self, *args, **kw):
        if "sa_pool_key" in kw:
            return kw["sa_pool_key"]

        return tuple(list(args) + [(k, kw[k]) for k in sorted(kw)])
