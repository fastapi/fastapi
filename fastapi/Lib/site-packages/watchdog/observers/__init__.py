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
:module: watchdog.observers
:synopsis: Observer that picks a native implementation if available.
:author: yesudeep@google.com (Yesudeep Mangalapilly)
:author: contact@tiger-222.fr (Mickaël Schoentgen)

Classes
=======
.. autoclass:: Observer
   :members:
   :show-inheritance:
   :inherited-members:

Observer thread that schedules watching directories and dispatches
calls to event handlers.

You can also import platform specific classes directly and use it instead
of :class:`Observer`.  Here is a list of implemented observer classes.:

============== ================================ ==============================
Class          Platforms                        Note
============== ================================ ==============================
|Inotify|      Linux 2.6.13+                    ``inotify(7)`` based observer
|FSEvents|     macOS                            FSEvents based observer
|Kqueue|       macOS and BSD with kqueue(2)     ``kqueue(2)`` based observer
|WinApi|       MS Windows                       Windows API-based observer
|Polling|      Any                              fallback implementation
============== ================================ ==============================

.. |Inotify|     replace:: :class:`.inotify.InotifyObserver`
.. |FSEvents|    replace:: :class:`.fsevents.FSEventsObserver`
.. |Kqueue|      replace:: :class:`.kqueue.KqueueObserver`
.. |WinApi|      replace:: :class:`.read_directory_changes.WindowsApiObserver`
.. |Polling|     replace:: :class:`.polling.PollingObserver`

"""

from __future__ import annotations

import sys
import warnings

from watchdog.utils import UnsupportedLibc

from .api import BaseObserverSubclassCallable

Observer: BaseObserverSubclassCallable


if sys.platform.startswith("linux"):
    try:
        from .inotify import InotifyObserver as Observer
    except UnsupportedLibc:
        from .polling import PollingObserver as Observer

elif sys.platform.startswith("darwin"):
    try:
        from .fsevents import FSEventsObserver as Observer
    except Exception:
        try:
            from .kqueue import KqueueObserver as Observer

            warnings.warn("Failed to import fsevents. Fall back to kqueue")
        except Exception:
            from .polling import PollingObserver as Observer

            warnings.warn("Failed to import fsevents and kqueue. Fall back to polling.")

elif sys.platform in ("dragonfly", "freebsd", "netbsd", "openbsd", "bsd"):
    from .kqueue import KqueueObserver as Observer

elif sys.platform.startswith("win"):
    try:
        from .read_directory_changes import WindowsApiObserver as Observer
    except Exception:
        from .polling import PollingObserver as Observer

        warnings.warn("Failed to import read_directory_changes. Fall back to polling.")

else:
    from .polling import PollingObserver as Observer

__all__ = ["Observer"]
