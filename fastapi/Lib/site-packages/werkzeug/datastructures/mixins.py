from __future__ import annotations

from itertools import repeat

from .._internal import _missing


def is_immutable(self):
    raise TypeError(f"{type(self).__name__!r} objects are immutable")


class ImmutableListMixin:
    """Makes a :class:`list` immutable.

    .. versionadded:: 0.5

    :private:
    """

    _hash_cache = None

    def __hash__(self):
        if self._hash_cache is not None:
            return self._hash_cache
        rv = self._hash_cache = hash(tuple(self))
        return rv

    def __reduce_ex__(self, protocol):
        return type(self), (list(self),)

    def __delitem__(self, key):
        is_immutable(self)

    def __iadd__(self, other):
        is_immutable(self)

    def __imul__(self, other):
        is_immutable(self)

    def __setitem__(self, key, value):
        is_immutable(self)

    def append(self, item):
        is_immutable(self)

    def remove(self, item):
        is_immutable(self)

    def extend(self, iterable):
        is_immutable(self)

    def insert(self, pos, value):
        is_immutable(self)

    def pop(self, index=-1):
        is_immutable(self)

    def reverse(self):
        is_immutable(self)

    def sort(self, key=None, reverse=False):
        is_immutable(self)


class ImmutableDictMixin:
    """Makes a :class:`dict` immutable.

    .. versionadded:: 0.5

    :private:
    """

    _hash_cache = None

    @classmethod
    def fromkeys(cls, keys, value=None):
        instance = super().__new__(cls)
        instance.__init__(zip(keys, repeat(value)))
        return instance

    def __reduce_ex__(self, protocol):
        return type(self), (dict(self),)

    def _iter_hashitems(self):
        return self.items()

    def __hash__(self):
        if self._hash_cache is not None:
            return self._hash_cache
        rv = self._hash_cache = hash(frozenset(self._iter_hashitems()))
        return rv

    def setdefault(self, key, default=None):
        is_immutable(self)

    def update(self, *args, **kwargs):
        is_immutable(self)

    def pop(self, key, default=None):
        is_immutable(self)

    def popitem(self):
        is_immutable(self)

    def __setitem__(self, key, value):
        is_immutable(self)

    def __delitem__(self, key):
        is_immutable(self)

    def clear(self):
        is_immutable(self)


class ImmutableMultiDictMixin(ImmutableDictMixin):
    """Makes a :class:`MultiDict` immutable.

    .. versionadded:: 0.5

    :private:
    """

    def __reduce_ex__(self, protocol):
        return type(self), (list(self.items(multi=True)),)

    def _iter_hashitems(self):
        return self.items(multi=True)

    def add(self, key, value):
        is_immutable(self)

    def popitemlist(self):
        is_immutable(self)

    def poplist(self, key):
        is_immutable(self)

    def setlist(self, key, new_list):
        is_immutable(self)

    def setlistdefault(self, key, default_list=None):
        is_immutable(self)


class ImmutableHeadersMixin:
    """Makes a :class:`Headers` immutable.  We do not mark them as
    hashable though since the only usecase for this datastructure
    in Werkzeug is a view on a mutable structure.

    .. versionadded:: 0.5

    :private:
    """

    def __delitem__(self, key, **kwargs):
        is_immutable(self)

    def __setitem__(self, key, value):
        is_immutable(self)

    def set(self, _key, _value, **kwargs):
        is_immutable(self)

    def setlist(self, key, values):
        is_immutable(self)

    def add(self, _key, _value, **kwargs):
        is_immutable(self)

    def add_header(self, _key, _value, **_kwargs):
        is_immutable(self)

    def remove(self, key):
        is_immutable(self)

    def extend(self, *args, **kwargs):
        is_immutable(self)

    def update(self, *args, **kwargs):
        is_immutable(self)

    def insert(self, pos, value):
        is_immutable(self)

    def pop(self, key=None, default=_missing):
        is_immutable(self)

    def popitem(self):
        is_immutable(self)

    def setdefault(self, key, default):
        is_immutable(self)

    def setlistdefault(self, key, default):
        is_immutable(self)


def _calls_update(name):
    def oncall(self, *args, **kw):
        rv = getattr(super(UpdateDictMixin, self), name)(*args, **kw)

        if self.on_update is not None:
            self.on_update(self)

        return rv

    oncall.__name__ = name
    return oncall


class UpdateDictMixin(dict):
    """Makes dicts call `self.on_update` on modifications.

    .. versionadded:: 0.5

    :private:
    """

    on_update = None

    def setdefault(self, key, default=None):
        modified = key not in self
        rv = super().setdefault(key, default)
        if modified and self.on_update is not None:
            self.on_update(self)
        return rv

    def pop(self, key, default=_missing):
        modified = key in self
        if default is _missing:
            rv = super().pop(key)
        else:
            rv = super().pop(key, default)
        if modified and self.on_update is not None:
            self.on_update(self)
        return rv

    __setitem__ = _calls_update("__setitem__")
    __delitem__ = _calls_update("__delitem__")
    clear = _calls_update("clear")
    popitem = _calls_update("popitem")
    update = _calls_update("update")
