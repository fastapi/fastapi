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
:module: watchdog.utils
:synopsis: Utility classes and functions.
:author: yesudeep@google.com (Yesudeep Mangalapilly)
:author: contact@tiger-222.fr (Mickaël Schoentgen)

Classes
-------
.. autoclass:: BaseThread
   :members:
   :show-inheritance:
   :inherited-members:

"""
from __future__ import annotations

import sys
import threading
from typing import TYPE_CHECKING


class UnsupportedLibc(Exception):
    pass


class WatchdogShutdown(Exception):
    """
    Semantic exception used to signal an external shutdown event.
    """

    pass


class BaseThread(threading.Thread):
    """Convenience class for creating stoppable threads."""

    def __init__(self):
        threading.Thread.__init__(self)
        if hasattr(self, "daemon"):
            self.daemon = True
        else:
            self.setDaemon(True)
        self._stopped_event = threading.Event()

    @property
    def stopped_event(self):
        return self._stopped_event

    def should_keep_running(self):
        """Determines whether the thread should continue running."""
        return not self._stopped_event.is_set()

    def on_thread_stop(self):
        """Override this method instead of :meth:`stop()`.
        :meth:`stop()` calls this method.

        This method is called immediately after the thread is signaled to stop.
        """
        pass

    def stop(self):
        """Signals the thread to stop."""
        self._stopped_event.set()
        self.on_thread_stop()

    def on_thread_start(self):
        """Override this method instead of :meth:`start()`. :meth:`start()`
        calls this method.

        This method is called right before this thread is started and this
        object’s run() method is invoked.
        """
        pass

    def start(self):
        self.on_thread_start()
        threading.Thread.start(self)


def load_module(module_name):
    """Imports a module given its name and returns a handle to it."""
    try:
        __import__(module_name)
    except ImportError:
        raise ImportError(f"No module named {module_name}")
    return sys.modules[module_name]


def load_class(dotted_path):
    """Loads and returns a class definition provided a dotted path
    specification the last part of the dotted path is the class name
    and there is at least one module name preceding the class name.

    Notes:
    You will need to ensure that the module you are trying to load
    exists in the Python path.

    Examples:
    - module.name.ClassName    # Provided module.name is in the Python path.
    - module.ClassName         # Provided module is in the Python path.

    What won't work:
    - ClassName
    - modle.name.ClassName     # Typo in module name.
    - module.name.ClasNam      # Typo in classname.
    """
    dotted_path_split = dotted_path.split(".")
    if len(dotted_path_split) <= 1:
        raise ValueError(
            f"Dotted module path {dotted_path} must contain a module name and a classname"
        )
    klass_name = dotted_path_split[-1]
    module_name = ".".join(dotted_path_split[:-1])

    module = load_module(module_name)
    if hasattr(module, klass_name):
        return getattr(module, klass_name)
        # Finally create and return an instance of the class
        # return klass(*args, **kwargs)
    else:
        raise AttributeError(
            f"Module {module_name} does not have class attribute {klass_name}"
        )


if TYPE_CHECKING or sys.version_info >= (3, 8):
    # using `as` to explicitly re-export this since this is a compatibility layer
    from typing import Protocol as Protocol
else:
    # Provide a dummy Protocol class when not available from stdlib.  Should be used
    # only for hinting.  This could be had from typing_protocol, but not worth adding
    # the _first_ dependency just for this.
    class Protocol:
        ...
