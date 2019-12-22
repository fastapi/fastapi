from contextvars import ContextVar

import peewee

DATABASE_NAME = "test.db"


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", {})
        self._state["closed"] = ContextVar("closed", default=True)
        self._state["conn"] = ContextVar("conn", default=None)
        self._state["ctx"] = ContextVar("ctx", default=[])
        self._state["transactions"] = ContextVar("transactions", default=[])
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state[name].set(value)

    def __getattr__(self, name):
        return self._state[name].get()


db = peewee.SqliteDatabase(DATABASE_NAME, check_same_thread=False)

db._state = PeeweeConnectionState()
