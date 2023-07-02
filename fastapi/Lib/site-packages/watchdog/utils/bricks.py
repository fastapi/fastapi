# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google, Inc & contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Utility collections or "bricks".

:module: watchdog.utils.bricks
:author: yesudeep@google.com (Yesudeep Mangalapilly)
:author: lalinsky@gmail.com (Lukáš Lalinský)
:author: python@rcn.com (Raymond Hettinger)
:author: contact@tiger-222.fr (Mickaël Schoentgen)

Classes
=======
.. autoclass:: OrderedSetQueue
   :members:
   :show-inheritance:
   :inherited-members:

.. autoclass:: OrderedSet

"""

from __future__ import annotations

import queue


class SkipRepeatsQueue(queue.Queue):

    """Thread-safe implementation of an special queue where a
    put of the last-item put'd will be dropped.

    The implementation leverages locking already implemented in the base class
    redefining only the primitives.

    Queued items must be immutable and hashable so that they can be used
    as dictionary keys. You must implement **only read-only properties** and
    the :meth:`Item.__hash__()`, :meth:`Item.__eq__()`, and
    :meth:`Item.__ne__()` methods for items to be hashable.

    An example implementation follows::

        class Item:
            def __init__(self, a, b):
                self._a = a
                self._b = b

            @property
            def a(self):
                return self._a

            @property
            def b(self):
                return self._b

            def _key(self):
                return (self._a, self._b)

            def __eq__(self, item):
                return self._key() == item._key()

            def __ne__(self, item):
                return self._key() != item._key()

            def __hash__(self):
                return hash(self._key())

    based on the OrderedSetQueue below
    """

    def _init(self, maxsize):
        super()._init(maxsize)
        self._last_item = None

    def _put(self, item):
        if self._last_item is None or item != self._last_item:
            super()._put(item)
            self._last_item = item
        else:
            # `put` increments `unfinished_tasks` even if we did not put
            # anything into the queue here
            self.unfinished_tasks -= 1

    def _get(self):
        item = super()._get()
        if item is self._last_item:
            self._last_item = None
        return item
