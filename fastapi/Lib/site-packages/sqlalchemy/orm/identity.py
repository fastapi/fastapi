# orm/identity.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

import weakref

from .. import exc as sa_exc
from .. import util
from . import util as orm_util


class IdentityMap(object):
    def __init__(self):
        self._dict = {}
        self._modified = set()
        self._wr = weakref.ref(self)

    def _kill(self):
        self._add_unpresent = _killed

    def keys(self):
        return self._dict.keys()

    def replace(self, state):
        raise NotImplementedError()

    def add(self, state):
        raise NotImplementedError()

    def _add_unpresent(self, state, key):
        """optional inlined form of add() which can assume item isn't present
        in the map"""
        self.add(state)

    def update(self, dict_):
        raise NotImplementedError("IdentityMap uses add() to insert data")

    def clear(self):
        raise NotImplementedError("IdentityMap uses remove() to remove data")

    def _manage_incoming_state(self, state):
        state._instance_dict = self._wr

        if state.modified:
            self._modified.add(state)

    def _manage_removed_state(self, state):
        del state._instance_dict
        if state.modified:
            self._modified.discard(state)

    def _dirty_states(self):
        return self._modified

    def check_modified(self):
        """return True if any InstanceStates present have been marked
        as 'modified'.

        """
        return bool(self._modified)

    def has_key(self, key):
        return key in self

    def popitem(self):
        raise NotImplementedError("IdentityMap uses remove() to remove data")

    def pop(self, key, *args):
        raise NotImplementedError("IdentityMap uses remove() to remove data")

    def setdefault(self, key, default=None):
        raise NotImplementedError("IdentityMap uses add() to insert data")

    def __len__(self):
        return len(self._dict)

    def copy(self):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        raise NotImplementedError("IdentityMap uses add() to insert data")

    def __delitem__(self, key):
        raise NotImplementedError("IdentityMap uses remove() to remove data")


class WeakInstanceDict(IdentityMap):
    def __getitem__(self, key):
        state = self._dict[key]
        o = state.obj()
        if o is None:
            raise KeyError(key)
        return o

    def __contains__(self, key):
        try:
            if key in self._dict:
                state = self._dict[key]
                o = state.obj()
            else:
                return False
        except KeyError:
            return False
        else:
            return o is not None

    def contains_state(self, state):
        if state.key in self._dict:
            try:
                return self._dict[state.key] is state
            except KeyError:
                return False
        else:
            return False

    def replace(self, state):
        if state.key in self._dict:
            try:
                existing = self._dict[state.key]
            except KeyError:
                # catch gc removed the key after we just checked for it
                pass
            else:
                if existing is not state:
                    self._manage_removed_state(existing)
                else:
                    return None
        else:
            existing = None

        self._dict[state.key] = state
        self._manage_incoming_state(state)
        return existing

    def add(self, state):
        key = state.key
        # inline of self.__contains__
        if key in self._dict:
            try:
                existing_state = self._dict[key]
            except KeyError:
                # catch gc removed the key after we just checked for it
                pass
            else:
                if existing_state is not state:
                    o = existing_state.obj()
                    if o is not None:
                        raise sa_exc.InvalidRequestError(
                            "Can't attach instance "
                            "%s; another instance with key %s is already "
                            "present in this session."
                            % (orm_util.state_str(state), state.key)
                        )
                else:
                    return False
        self._dict[key] = state
        self._manage_incoming_state(state)
        return True

    def _add_unpresent(self, state, key):
        # inlined form of add() called by loading.py
        self._dict[key] = state
        state._instance_dict = self._wr

    def get(self, key, default=None):
        if key not in self._dict:
            return default
        try:
            state = self._dict[key]
        except KeyError:
            # catch gc removed the key after we just checked for it
            return default
        else:
            o = state.obj()
            if o is None:
                return default
            return o

    def items(self):
        values = self.all_states()
        result = []
        for state in values:
            value = state.obj()
            if value is not None:
                result.append((state.key, value))
        return result

    def values(self):
        values = self.all_states()
        result = []
        for state in values:
            value = state.obj()
            if value is not None:
                result.append(value)

        return result

    def __iter__(self):
        return iter(self.keys())

    if util.py2k:

        def iteritems(self):
            return iter(self.items())

        def itervalues(self):
            return iter(self.values())

    def all_states(self):
        if util.py2k:
            return self._dict.values()
        else:
            return list(self._dict.values())

    def _fast_discard(self, state):
        # used by InstanceState for state being
        # GC'ed, inlines _managed_removed_state
        try:
            st = self._dict[state.key]
        except KeyError:
            # catch gc removed the key after we just checked for it
            pass
        else:
            if st is state:
                self._dict.pop(state.key, None)

    def discard(self, state):
        self.safe_discard(state)

    def safe_discard(self, state):
        if state.key in self._dict:
            try:
                st = self._dict[state.key]
            except KeyError:
                # catch gc removed the key after we just checked for it
                pass
            else:
                if st is state:
                    self._dict.pop(state.key, None)
                    self._manage_removed_state(state)


def _killed(state, key):
    # external function to avoid creating cycles when assigned to
    # the IdentityMap
    raise sa_exc.InvalidRequestError(
        "Object %s cannot be converted to 'persistent' state, as this "
        "identity map is no longer valid.  Has the owning Session "
        "been closed?" % orm_util.state_str(state),
        code="lkrp",
    )
