import abc

from ..util import ABC


class ConnectionCharacteristic(ABC):
    """An abstract base for an object that can set, get and reset a
    per-connection characteristic, typically one that gets reset when the
    connection is returned to the connection pool.

    transaction isolation is the canonical example, and the
    ``IsolationLevelCharacteristic`` implementation provides this for the
    ``DefaultDialect``.

    The ``ConnectionCharacteristic`` class should call upon the ``Dialect`` for
    the implementation of each method.   The object exists strictly to serve as
    a dialect visitor that can be placed into the
    ``DefaultDialect.connection_characteristics`` dictionary where it will take
    effect for calls to :meth:`_engine.Connection.execution_options` and
    related APIs.

    .. versionadded:: 1.4

    """

    __slots__ = ()

    transactional = False

    @abc.abstractmethod
    def reset_characteristic(self, dialect, dbapi_conn):
        """Reset the characteristic on the connection to its default value."""

    @abc.abstractmethod
    def set_characteristic(self, dialect, dbapi_conn, value):
        """set characteristic on the connection to a given value."""

    @abc.abstractmethod
    def get_characteristic(self, dialect, dbapi_conn):
        """Given a DBAPI connection, get the current value of the
        characteristic.

        """


class IsolationLevelCharacteristic(ConnectionCharacteristic):
    transactional = True

    def reset_characteristic(self, dialect, dbapi_conn):
        dialect.reset_isolation_level(dbapi_conn)

    def set_characteristic(self, dialect, dbapi_conn, value):
        dialect.set_isolation_level(dbapi_conn, value)

    def get_characteristic(self, dialect, dbapi_conn):
        return dialect.get_isolation_level(dbapi_conn)
