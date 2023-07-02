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
:module: watchdog.observers.fsevents
:synopsis: FSEvents based emitter implementation.
:author: yesudeep@google.com (Yesudeep Mangalapilly)
:author: contact@tiger-222.fr (Mickaël Schoentgen)
:platforms: macOS
"""

from __future__ import annotations

import logging
import os
import threading
import time
import unicodedata

import _watchdog_fsevents as _fsevents  # type: ignore[import]

from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    generate_sub_created_events,
    generate_sub_moved_events,
)
from watchdog.observers.api import (
    DEFAULT_EMITTER_TIMEOUT,
    DEFAULT_OBSERVER_TIMEOUT,
    BaseObserver,
    EventEmitter,
)
from watchdog.utils.dirsnapshot import DirectorySnapshot

logger = logging.getLogger("fsevents")


class FSEventsEmitter(EventEmitter):

    """
    macOS FSEvents Emitter class.

    :param event_queue:
        The event queue to fill with events.
    :param watch:
        A watch object representing the directory to monitor.
    :type watch:
        :class:`watchdog.observers.api.ObservedWatch`
    :param timeout:
        Read events blocking timeout (in seconds).
    :param suppress_history:
        The FSEvents API may emit historic events up to 30 sec before the watch was
        started. When ``suppress_history`` is ``True``, those events will be suppressed
        by creating a directory snapshot of the watched path before starting the stream
        as a reference to suppress old events. Warning: This may result in significant
        memory usage in case of a large number of items in the watched path.
    :type timeout:
        ``float``
    """

    def __init__(
        self,
        event_queue,
        watch,
        timeout=DEFAULT_EMITTER_TIMEOUT,
        suppress_history=False,
    ):
        super().__init__(event_queue, watch, timeout)
        self._fs_view = set()
        self.suppress_history = suppress_history
        self._start_time = 0.0
        self._starting_state = None
        self._lock = threading.Lock()
        self._absolute_watch_path = os.path.realpath(
            os.path.abspath(os.path.expanduser(self.watch.path))
        )

    def on_thread_stop(self):
        _fsevents.remove_watch(self.watch)
        _fsevents.stop(self)

    def queue_event(self, event):
        # fsevents defaults to be recursive, so if the watch was meant to be non-recursive then we need to drop
        # all the events here which do not have a src_path / dest_path that matches the watched path
        if self._watch.is_recursive:
            logger.debug("queue_event %s", event)
            EventEmitter.queue_event(self, event)
        else:
            if not self._is_recursive_event(event):
                logger.debug("queue_event %s", event)
                EventEmitter.queue_event(self, event)
            else:
                logger.debug("drop event %s", event)

    def _is_recursive_event(self, event):
        src_path = (
            event.src_path if event.is_directory else os.path.dirname(event.src_path)
        )
        if src_path == self._absolute_watch_path:
            return False

        if isinstance(event, (FileMovedEvent, DirMovedEvent)):
            # when moving something into the watch path we must always take the dirname,
            # otherwise we miss out on `DirMovedEvent`s
            dest_path = os.path.dirname(event.dest_path)
            if dest_path == self._absolute_watch_path:
                return False

        return True

    def _queue_created_event(self, event, src_path, dirname):
        cls = DirCreatedEvent if event.is_directory else FileCreatedEvent
        self.queue_event(cls(src_path))
        self.queue_event(DirModifiedEvent(dirname))

    def _queue_deleted_event(self, event, src_path, dirname):
        cls = DirDeletedEvent if event.is_directory else FileDeletedEvent
        self.queue_event(cls(src_path))
        self.queue_event(DirModifiedEvent(dirname))

    def _queue_modified_event(self, event, src_path, dirname):
        cls = DirModifiedEvent if event.is_directory else FileModifiedEvent
        self.queue_event(cls(src_path))

    def _queue_renamed_event(
        self, src_event, src_path, dst_path, src_dirname, dst_dirname
    ):
        cls = DirMovedEvent if src_event.is_directory else FileMovedEvent
        dst_path = self._encode_path(dst_path)
        self.queue_event(cls(src_path, dst_path))
        self.queue_event(DirModifiedEvent(src_dirname))
        self.queue_event(DirModifiedEvent(dst_dirname))

    def _is_historic_created_event(self, event):
        # We only queue a created event if the item was created after we
        # started the FSEventsStream.

        in_history = event.inode in self._fs_view

        if self._starting_state:
            try:
                old_inode = self._starting_state.inode(event.path)[0]
                before_start = old_inode == event.inode
            except KeyError:
                before_start = False
        else:
            before_start = False

        return in_history or before_start

    @staticmethod
    def _is_meta_mod(event):
        """Returns True if the event indicates a change in metadata."""
        return event.is_inode_meta_mod or event.is_xattr_mod or event.is_owner_change

    def queue_events(self, timeout, events):
        if logger.getEffectiveLevel() <= logging.DEBUG:
            for event in events:
                flags = ", ".join(
                    attr for attr in dir(event) if getattr(event, attr) is True
                )
                logger.debug(f"{event}: {flags}")

        if time.monotonic() - self._start_time > 60:
            # Event history is no longer needed, let's free some memory.
            self._starting_state = None

        while events:
            event = events.pop(0)

            src_path = self._encode_path(event.path)
            src_dirname = os.path.dirname(src_path)

            try:
                stat = os.stat(src_path)
            except OSError:
                stat = None

            exists = stat and stat.st_ino == event.inode

            # FSevents may coalesce multiple events for the same item + path into a
            # single event. However, events are never coalesced for different items at
            # the same path or for the same item at different paths. Therefore, the
            # event chains "removed -> created" and "created -> renamed -> removed" will
            # never emit a single native event and a deleted event *always* means that
            # the item no longer existed at the end of the event chain.

            # Some events will have a spurious `is_created` flag set, coalesced from an
            # already emitted and processed CreatedEvent. To filter those, we keep track
            # of all inodes which we know to be already created. This is safer than
            # keeping track of paths since paths are more likely to be reused than
            # inodes.

            # Likewise, some events will have a spurious `is_modified`,
            # `is_inode_meta_mod` or `is_xattr_mod` flag set. We currently do not
            # suppress those but could do so if the item still exists by caching the
            # stat result and verifying that it did change.

            if event.is_created and event.is_removed:
                # Events will only be coalesced for the same item / inode.
                # The sequence deleted -> created therefore cannot occur.
                # Any combination with renamed cannot occur either.

                if not self._is_historic_created_event(event):
                    self._queue_created_event(event, src_path, src_dirname)

                self._fs_view.add(event.inode)

                if event.is_modified or self._is_meta_mod(event):
                    self._queue_modified_event(event, src_path, src_dirname)

                self._queue_deleted_event(event, src_path, src_dirname)
                self._fs_view.discard(event.inode)

            else:
                if event.is_created and not self._is_historic_created_event(event):
                    self._queue_created_event(event, src_path, src_dirname)

                self._fs_view.add(event.inode)

                if event.is_modified or self._is_meta_mod(event):
                    self._queue_modified_event(event, src_path, src_dirname)

                if event.is_renamed:
                    # Check if we have a corresponding destination event in the watched path.
                    dst_event = next(
                        iter(
                            e for e in events if e.is_renamed and e.inode == event.inode
                        ),
                        None,
                    )

                    if dst_event:
                        # Item was moved within the watched folder.
                        logger.debug("Destination event for rename is %s", dst_event)

                        dst_path = self._encode_path(dst_event.path)
                        dst_dirname = os.path.dirname(dst_path)

                        self._queue_renamed_event(
                            event, src_path, dst_path, src_dirname, dst_dirname
                        )
                        self._fs_view.add(event.inode)

                        for sub_event in generate_sub_moved_events(src_path, dst_path):
                            self.queue_event(sub_event)

                        # Process any coalesced flags for the dst_event.

                        events.remove(dst_event)

                        if dst_event.is_modified or self._is_meta_mod(dst_event):
                            self._queue_modified_event(dst_event, dst_path, dst_dirname)

                        if dst_event.is_removed:
                            self._queue_deleted_event(dst_event, dst_path, dst_dirname)
                            self._fs_view.discard(dst_event.inode)

                    elif exists:
                        # This is the destination event, item was moved into the watched
                        # folder.
                        self._queue_created_event(event, src_path, src_dirname)
                        self._fs_view.add(event.inode)

                        for sub_event in generate_sub_created_events(src_path):
                            self.queue_event(sub_event)

                    else:
                        # This is the source event, item was moved out of the watched
                        # folder.
                        self._queue_deleted_event(event, src_path, src_dirname)
                        self._fs_view.discard(event.inode)

                        # Skip further coalesced processing.
                        continue

                if event.is_removed:
                    # Won't occur together with renamed.
                    self._queue_deleted_event(event, src_path, src_dirname)
                    self._fs_view.discard(event.inode)

            if event.is_root_changed:
                # This will be set if root or any of its parents is renamed or deleted.
                # TODO: find out new path and generate DirMovedEvent?
                self.queue_event(DirDeletedEvent(self.watch.path))
                logger.debug("Stopping because root path was changed")
                self.stop()

                self._fs_view.clear()

    def events_callback(self, paths, inodes, flags, ids):
        """Callback passed to FSEventStreamCreate(), it will receive all
        FS events and queue them.
        """
        cls = _fsevents.NativeEvent
        try:
            events = [
                cls(path, inode, event_flags, event_id)
                for path, inode, event_flags, event_id in zip(paths, inodes, flags, ids)
            ]
            with self._lock:
                self.queue_events(self.timeout, events)
        except Exception:
            logger.exception("Unhandled exception in fsevents callback")

    def run(self):
        self.pathnames = [self.watch.path]
        self._start_time = time.monotonic()
        try:
            _fsevents.add_watch(self, self.watch, self.events_callback, self.pathnames)
            _fsevents.read_events(self)
        except Exception:
            logger.exception("Unhandled exception in FSEventsEmitter")

    def on_thread_start(self):
        if self.suppress_history:
            if isinstance(self.watch.path, bytes):
                watch_path = os.fsdecode(self.watch.path)
            else:
                watch_path = self.watch.path

            self._starting_state = DirectorySnapshot(watch_path)

    def _encode_path(self, path):
        """Encode path only if bytes were passed to this emitter."""
        if isinstance(self.watch.path, bytes):
            return os.fsencode(path)
        return path


class FSEventsObserver(BaseObserver):
    def __init__(self, timeout=DEFAULT_OBSERVER_TIMEOUT):
        super().__init__(emitter_class=FSEventsEmitter, timeout=timeout)

    def schedule(self, event_handler, path, recursive=False):
        # Fix for issue #26: Trace/BPT error when given a unicode path
        # string. https://github.com/gorakhargosh/watchdog/issues#issue/26
        if isinstance(path, str):
            path = unicodedata.normalize("NFC", path)
        return BaseObserver.schedule(self, event_handler, path, recursive)
