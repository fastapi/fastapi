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
:module: watchdog.tricks
:synopsis: Utility event handlers.
:author: yesudeep@google.com (Yesudeep Mangalapilly)
:author: contact@tiger-222.fr (Mickaël Schoentgen)

Classes
-------
.. autoclass:: Trick
   :members:
   :show-inheritance:

.. autoclass:: LoggerTrick
   :members:
   :show-inheritance:

.. autoclass:: ShellCommandTrick
   :members:
   :show-inheritance:

.. autoclass:: AutoRestartTrick
   :members:
   :show-inheritance:

"""

from __future__ import annotations

import functools
import logging
import os
import signal
import subprocess
import sys
import threading
import time

from watchdog.events import EVENT_TYPE_OPENED, PatternMatchingEventHandler
from watchdog.utils import echo
from watchdog.utils.event_debouncer import EventDebouncer
from watchdog.utils.process_watcher import ProcessWatcher

logger = logging.getLogger(__name__)
echo_events = functools.partial(echo.echo, write=lambda msg: logger.info(msg))


class Trick(PatternMatchingEventHandler):

    """Your tricks should subclass this class."""

    @classmethod
    def generate_yaml(cls):
        return f"""- {cls.__module__}.{cls.__name__}:
  args:
  - argument1
  - argument2
  kwargs:
    patterns:
    - "*.py"
    - "*.js"
    ignore_patterns:
    - "version.py"
    ignore_directories: false
"""


class LoggerTrick(Trick):

    """A simple trick that does only logs events."""

    def on_any_event(self, event):
        pass

    @echo_events
    def on_modified(self, event):
        pass

    @echo_events
    def on_deleted(self, event):
        pass

    @echo_events
    def on_created(self, event):
        pass

    @echo_events
    def on_moved(self, event):
        pass

    @echo_events
    def on_closed(self, event):
        pass

    @echo_events
    def on_opened(self, event):
        pass


class ShellCommandTrick(Trick):

    """Executes shell commands in response to matched events."""

    def __init__(
        self,
        shell_command=None,
        patterns=None,
        ignore_patterns=None,
        ignore_directories=False,
        wait_for_process=False,
        drop_during_process=False,
    ):
        super().__init__(
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=ignore_directories,
        )
        self.shell_command = shell_command
        self.wait_for_process = wait_for_process
        self.drop_during_process = drop_during_process

        self.process = None
        self._process_watchers = set()

    def on_any_event(self, event):
        if event.event_type == EVENT_TYPE_OPENED:
            # FIXME: see issue #949, and find a way to better handle that scenario
            return

        from string import Template

        if self.drop_during_process and self.is_process_running():
            return

        object_type = "directory" if event.is_directory else "file"
        context = {
            "watch_src_path": event.src_path,
            "watch_dest_path": "",
            "watch_event_type": event.event_type,
            "watch_object": object_type,
        }

        if self.shell_command is None:
            if hasattr(event, "dest_path"):
                context["dest_path"] = event.dest_path
                command = 'echo "${watch_event_type} ${watch_object} from ${watch_src_path} to ${watch_dest_path}"'
            else:
                command = 'echo "${watch_event_type} ${watch_object} ${watch_src_path}"'
        else:
            if hasattr(event, "dest_path"):
                context["watch_dest_path"] = event.dest_path
            command = self.shell_command

        command = Template(command).safe_substitute(**context)
        self.process = subprocess.Popen(command, shell=True)
        if self.wait_for_process:
            self.process.wait()
        else:
            process_watcher = ProcessWatcher(self.process, None)
            self._process_watchers.add(process_watcher)
            process_watcher.process_termination_callback = functools.partial(
                self._process_watchers.discard, process_watcher
            )
            process_watcher.start()

    def is_process_running(self):
        return self._process_watchers or (
            self.process is not None and self.process.poll() is None
        )


class AutoRestartTrick(Trick):

    """Starts a long-running subprocess and restarts it on matched events.

    The command parameter is a list of command arguments, such as
    `['bin/myserver', '-c', 'etc/myconfig.ini']`.

    Call `start()` after creating the Trick. Call `stop()` when stopping
    the process.
    """

    def __init__(
        self,
        command,
        patterns=None,
        ignore_patterns=None,
        ignore_directories=False,
        stop_signal=signal.SIGINT,
        kill_after=10,
        debounce_interval_seconds=0,
        restart_on_command_exit=True,
    ):
        if kill_after < 0:
            raise ValueError("kill_after must be non-negative.")
        if debounce_interval_seconds < 0:
            raise ValueError("debounce_interval_seconds must be non-negative.")

        super().__init__(
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=ignore_directories,
        )

        self.command = command
        self.stop_signal = stop_signal
        self.kill_after = kill_after
        self.debounce_interval_seconds = debounce_interval_seconds
        self.restart_on_command_exit = restart_on_command_exit

        self.process = None
        self.process_watcher = None
        self.event_debouncer = None
        self.restart_count = 0

        self._is_process_stopping = False
        self._is_trick_stopping = False
        self._stopping_lock = threading.RLock()

    def start(self):
        if self.debounce_interval_seconds:
            self.event_debouncer = EventDebouncer(
                debounce_interval_seconds=self.debounce_interval_seconds,
                events_callback=lambda events: self._restart_process(),
            )
            self.event_debouncer.start()
        self._start_process()

    def stop(self):
        # Ensure the body of the function is only run once.
        with self._stopping_lock:
            if self._is_trick_stopping:
                return
            self._is_trick_stopping = True

        process_watcher = self.process_watcher
        if self.event_debouncer is not None:
            self.event_debouncer.stop()
        self._stop_process()

        # Don't leak threads: Wait for background threads to stop.
        if self.event_debouncer is not None:
            self.event_debouncer.join()
        if process_watcher is not None:
            process_watcher.join()

    def _start_process(self):
        if self._is_trick_stopping:
            return

        # windows doesn't have setsid
        self.process = subprocess.Popen(
            self.command, preexec_fn=getattr(os, "setsid", None)
        )
        if self.restart_on_command_exit:
            self.process_watcher = ProcessWatcher(self.process, self._restart_process)
            self.process_watcher.start()

    def _stop_process(self):
        # Ensure the body of the function is not run in parallel in different threads.
        with self._stopping_lock:
            if self._is_process_stopping:
                return
            self._is_process_stopping = True

        try:
            if self.process_watcher is not None:
                self.process_watcher.stop()
                self.process_watcher = None

            if self.process is not None:
                try:
                    kill_process(self.process.pid, self.stop_signal)
                except OSError:
                    # Process is already gone
                    pass
                else:
                    kill_time = time.time() + self.kill_after
                    while time.time() < kill_time:
                        if self.process.poll() is not None:
                            break
                        time.sleep(0.25)
                    else:
                        try:
                            kill_process(self.process.pid, 9)
                        except OSError:
                            # Process is already gone
                            pass
                self.process = None
        finally:
            self._is_process_stopping = False

    @echo_events
    def on_any_event(self, event):
        if event.event_type == EVENT_TYPE_OPENED:
            # FIXME: see issue #949, and find a way to better handle that scenario
            return

        if self.event_debouncer is not None:
            self.event_debouncer.handle_event(event)
        else:
            self._restart_process()

    def _restart_process(self):
        if self._is_trick_stopping:
            return
        self._stop_process()
        self._start_process()
        self.restart_count += 1


if not sys.platform.startswith("win"):

    def kill_process(pid, stop_signal):
        os.killpg(os.getpgid(pid), stop_signal)

else:

    def kill_process(pid, stop_signal):
        os.kill(pid, stop_signal)
