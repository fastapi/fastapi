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

from __future__ import annotations

import ctypes
import ctypes.util
import errno
import os
import struct
import threading
from ctypes import c_char_p, c_int, c_uint32
from functools import reduce

from watchdog.utils import UnsupportedLibc

libc = ctypes.CDLL(None)

if (
    not hasattr(libc, "inotify_init")
    or not hasattr(libc, "inotify_add_watch")
    or not hasattr(libc, "inotify_rm_watch")
):
    raise UnsupportedLibc(f"Unsupported libc version found: {libc._name}")

inotify_add_watch = ctypes.CFUNCTYPE(c_int, c_int, c_char_p, c_uint32, use_errno=True)(
    ("inotify_add_watch", libc)
)

inotify_rm_watch = ctypes.CFUNCTYPE(c_int, c_int, c_uint32, use_errno=True)(
    ("inotify_rm_watch", libc)
)

inotify_init = ctypes.CFUNCTYPE(c_int, use_errno=True)(("inotify_init", libc))


class InotifyConstants:
    # User-space events
    IN_ACCESS = 0x00000001  # File was accessed.
    IN_MODIFY = 0x00000002  # File was modified.
    IN_ATTRIB = 0x00000004  # Meta-data changed.
    IN_CLOSE_WRITE = 0x00000008  # Writable file was closed.
    IN_CLOSE_NOWRITE = 0x00000010  # Unwritable file closed.
    IN_OPEN = 0x00000020  # File was opened.
    IN_MOVED_FROM = 0x00000040  # File was moved from X.
    IN_MOVED_TO = 0x00000080  # File was moved to Y.
    IN_CREATE = 0x00000100  # Subfile was created.
    IN_DELETE = 0x00000200  # Subfile was deleted.
    IN_DELETE_SELF = 0x00000400  # Self was deleted.
    IN_MOVE_SELF = 0x00000800  # Self was moved.

    # Helper user-space events.
    IN_CLOSE = IN_CLOSE_WRITE | IN_CLOSE_NOWRITE  # Close.
    IN_MOVE = IN_MOVED_FROM | IN_MOVED_TO  # Moves.

    # Events sent by the kernel to a watch.
    IN_UNMOUNT = 0x00002000  # Backing file system was unmounted.
    IN_Q_OVERFLOW = 0x00004000  # Event queued overflowed.
    IN_IGNORED = 0x00008000  # File was ignored.

    # Special flags.
    IN_ONLYDIR = 0x01000000  # Only watch the path if it's a directory.
    IN_DONT_FOLLOW = 0x02000000  # Do not follow a symbolic link.
    IN_EXCL_UNLINK = 0x04000000  # Exclude events on unlinked objects
    IN_MASK_ADD = 0x20000000  # Add to the mask of an existing watch.
    IN_ISDIR = 0x40000000  # Event occurred against directory.
    IN_ONESHOT = 0x80000000  # Only send event once.

    # All user-space events.
    IN_ALL_EVENTS = reduce(
        lambda x, y: x | y,
        [
            IN_ACCESS,
            IN_MODIFY,
            IN_ATTRIB,
            IN_CLOSE_WRITE,
            IN_CLOSE_NOWRITE,
            IN_OPEN,
            IN_MOVED_FROM,
            IN_MOVED_TO,
            IN_DELETE,
            IN_CREATE,
            IN_DELETE_SELF,
            IN_MOVE_SELF,
        ],
    )

    # Flags for ``inotify_init1``
    IN_CLOEXEC = 0x02000000
    IN_NONBLOCK = 0x00004000


# Watchdog's API cares only about these events.
WATCHDOG_ALL_EVENTS = reduce(
    lambda x, y: x | y,
    [
        InotifyConstants.IN_MODIFY,
        InotifyConstants.IN_ATTRIB,
        InotifyConstants.IN_MOVED_FROM,
        InotifyConstants.IN_MOVED_TO,
        InotifyConstants.IN_CREATE,
        InotifyConstants.IN_DELETE,
        InotifyConstants.IN_DELETE_SELF,
        InotifyConstants.IN_DONT_FOLLOW,
        InotifyConstants.IN_CLOSE_WRITE,
        InotifyConstants.IN_OPEN,
    ],
)


class inotify_event_struct(ctypes.Structure):
    """
    Structure representation of the inotify_event structure
    (used in buffer size calculations)::

        struct inotify_event {
            __s32 wd;            /* watch descriptor */
            __u32 mask;          /* watch mask */
            __u32 cookie;        /* cookie to synchronize two events */
            __u32 len;           /* length (including nulls) of name */
            char  name[0];       /* stub for possible name */
        };
    """

    _fields_ = [
        ("wd", c_int),
        ("mask", c_uint32),
        ("cookie", c_uint32),
        ("len", c_uint32),
        ("name", c_char_p),
    ]


EVENT_SIZE = ctypes.sizeof(inotify_event_struct)
DEFAULT_NUM_EVENTS = 2048
DEFAULT_EVENT_BUFFER_SIZE = DEFAULT_NUM_EVENTS * (EVENT_SIZE + 16)


class Inotify:
    """
    Linux inotify(7) API wrapper class.

    :param path:
        The directory path for which we want an inotify object.
    :type path:
        :class:`bytes`
    :param recursive:
        ``True`` if subdirectories should be monitored; ``False`` otherwise.
    """

    def __init__(self, path, recursive=False, event_mask=WATCHDOG_ALL_EVENTS):
        # The file descriptor associated with the inotify instance.
        inotify_fd = inotify_init()
        if inotify_fd == -1:
            Inotify._raise_error()
        self._inotify_fd = inotify_fd
        self._lock = threading.Lock()

        # Stores the watch descriptor for a given path.
        self._wd_for_path = {}
        self._path_for_wd = {}

        self._path = path
        self._event_mask = event_mask
        self._is_recursive = recursive
        if os.path.isdir(path):
            self._add_dir_watch(path, recursive, event_mask)
        else:
            self._add_watch(path, event_mask)
        self._moved_from_events = {}

    @property
    def event_mask(self):
        """The event mask for this inotify instance."""
        return self._event_mask

    @property
    def path(self):
        """The path associated with the inotify instance."""
        return self._path

    @property
    def is_recursive(self):
        """Whether we are watching directories recursively."""
        return self._is_recursive

    @property
    def fd(self):
        """The file descriptor associated with the inotify instance."""
        return self._inotify_fd

    def clear_move_records(self):
        """Clear cached records of MOVED_FROM events"""
        self._moved_from_events = {}

    def source_for_move(self, destination_event):
        """
        The source path corresponding to the given MOVED_TO event.

        If the source path is outside the monitored directories, None
        is returned instead.
        """
        if destination_event.cookie in self._moved_from_events:
            return self._moved_from_events[destination_event.cookie].src_path
        else:
            return None

    def remember_move_from_event(self, event):
        """
        Save this event as the source event for future MOVED_TO events to
        reference.
        """
        self._moved_from_events[event.cookie] = event

    def add_watch(self, path):
        """
        Adds a watch for the given path.

        :param path:
            Path to begin monitoring.
        """
        with self._lock:
            self._add_watch(path, self._event_mask)

    def remove_watch(self, path):
        """
        Removes a watch for the given path.

        :param path:
            Path string for which the watch will be removed.
        """
        with self._lock:
            wd = self._wd_for_path.pop(path)
            del self._path_for_wd[wd]
            if inotify_rm_watch(self._inotify_fd, wd) == -1:
                Inotify._raise_error()

    def close(self):
        """
        Closes the inotify instance and removes all associated watches.
        """
        with self._lock:
            if self._path in self._wd_for_path:
                wd = self._wd_for_path[self._path]
                inotify_rm_watch(self._inotify_fd, wd)

            try:
                os.close(self._inotify_fd)
            except OSError:
                # descriptor may be invalid because file was deleted
                pass

    def read_events(self, event_buffer_size=DEFAULT_EVENT_BUFFER_SIZE):
        """
        Reads events from inotify and yields them.
        """
        # HACK: We need to traverse the directory path
        # recursively and simulate events for newly
        # created subdirectories/files. This will handle
        # mkdir -p foobar/blah/bar; touch foobar/afile

        def _recursive_simulate(src_path):
            events = []
            for root, dirnames, filenames in os.walk(src_path):
                for dirname in dirnames:
                    try:
                        full_path = os.path.join(root, dirname)
                        wd_dir = self._add_watch(full_path, self._event_mask)
                        e = InotifyEvent(
                            wd_dir,
                            InotifyConstants.IN_CREATE | InotifyConstants.IN_ISDIR,
                            0,
                            dirname,
                            full_path,
                        )
                        events.append(e)
                    except OSError:
                        pass
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    wd_parent_dir = self._wd_for_path[os.path.dirname(full_path)]
                    e = InotifyEvent(
                        wd_parent_dir,
                        InotifyConstants.IN_CREATE,
                        0,
                        filename,
                        full_path,
                    )
                    events.append(e)
            return events

        event_buffer = None
        while True:
            try:
                event_buffer = os.read(self._inotify_fd, event_buffer_size)
            except OSError as e:
                if e.errno == errno.EINTR:
                    continue
                elif e.errno == errno.EBADF:
                    return []
                else:
                    raise
            break

        with self._lock:
            event_list = []
            for wd, mask, cookie, name in Inotify._parse_event_buffer(event_buffer):
                if wd == -1:
                    continue
                wd_path = self._path_for_wd[wd]
                src_path = (
                    os.path.join(wd_path, name) if name else wd_path
                )  # avoid trailing slash
                inotify_event = InotifyEvent(wd, mask, cookie, name, src_path)

                if inotify_event.is_moved_from:
                    self.remember_move_from_event(inotify_event)
                elif inotify_event.is_moved_to:
                    move_src_path = self.source_for_move(inotify_event)
                    if move_src_path in self._wd_for_path:
                        moved_wd = self._wd_for_path[move_src_path]
                        del self._wd_for_path[move_src_path]
                        self._wd_for_path[inotify_event.src_path] = moved_wd
                        self._path_for_wd[moved_wd] = inotify_event.src_path
                        if self.is_recursive:
                            for _path, _wd in self._wd_for_path.copy().items():
                                if _path.startswith(
                                    move_src_path + os.path.sep.encode()
                                ):
                                    moved_wd = self._wd_for_path.pop(_path)
                                    _move_to_path = _path.replace(
                                        move_src_path, inotify_event.src_path
                                    )
                                    self._wd_for_path[_move_to_path] = moved_wd
                                    self._path_for_wd[moved_wd] = _move_to_path
                    src_path = os.path.join(wd_path, name)
                    inotify_event = InotifyEvent(wd, mask, cookie, name, src_path)

                if inotify_event.is_ignored:
                    # Clean up book-keeping for deleted watches.
                    path = self._path_for_wd.pop(wd)
                    if self._wd_for_path[path] == wd:
                        del self._wd_for_path[path]

                event_list.append(inotify_event)

                if (
                    self.is_recursive
                    and inotify_event.is_directory
                    and inotify_event.is_create
                ):
                    # TODO: When a directory from another part of the
                    # filesystem is moved into a watched directory, this
                    # will not generate events for the directory tree.
                    # We need to coalesce IN_MOVED_TO events and those
                    # IN_MOVED_TO events which don't pair up with
                    # IN_MOVED_FROM events should be marked IN_CREATE
                    # instead relative to this directory.
                    try:
                        self._add_watch(src_path, self._event_mask)
                    except OSError:
                        continue

                    event_list.extend(_recursive_simulate(src_path))

        return event_list

    # Non-synchronized methods.
    def _add_dir_watch(self, path, recursive, mask):
        """
        Adds a watch (optionally recursively) for the given directory path
        to monitor events specified by the mask.

        :param path:
            Path to monitor
        :param recursive:
            ``True`` to monitor recursively.
        :param mask:
            Event bit mask.
        """
        if not os.path.isdir(path):
            raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), path)
        self._add_watch(path, mask)
        if recursive:
            for root, dirnames, _ in os.walk(path):
                for dirname in dirnames:
                    full_path = os.path.join(root, dirname)
                    if os.path.islink(full_path):
                        continue
                    self._add_watch(full_path, mask)

    def _add_watch(self, path, mask):
        """
        Adds a watch for the given path to monitor events specified by the
        mask.

        :param path:
            Path to monitor
        :param mask:
            Event bit mask.
        """
        wd = inotify_add_watch(self._inotify_fd, path, mask)
        if wd == -1:
            Inotify._raise_error()
        self._wd_for_path[path] = wd
        self._path_for_wd[wd] = path
        return wd

    @staticmethod
    def _raise_error():
        """
        Raises errors for inotify failures.
        """
        err = ctypes.get_errno()
        if err == errno.ENOSPC:
            raise OSError(errno.ENOSPC, "inotify watch limit reached")
        elif err == errno.EMFILE:
            raise OSError(errno.EMFILE, "inotify instance limit reached")
        elif err != errno.EACCES:
            raise OSError(err, os.strerror(err))

    @staticmethod
    def _parse_event_buffer(event_buffer):
        """
        Parses an event buffer of ``inotify_event`` structs returned by
        inotify::

            struct inotify_event {
                __s32 wd;            /* watch descriptor */
                __u32 mask;          /* watch mask */
                __u32 cookie;        /* cookie to synchronize two events */
                __u32 len;           /* length (including nulls) of name */
                char  name[0];       /* stub for possible name */
            };

        The ``cookie`` member of this struct is used to pair two related
        events, for example, it pairs an IN_MOVED_FROM event with an
        IN_MOVED_TO event.
        """
        i = 0
        while i + 16 <= len(event_buffer):
            wd, mask, cookie, length = struct.unpack_from("iIII", event_buffer, i)
            name = event_buffer[i + 16 : i + 16 + length].rstrip(b"\0")
            i += 16 + length
            yield wd, mask, cookie, name


class InotifyEvent:
    """
    Inotify event struct wrapper.

    :param wd:
        Watch descriptor
    :param mask:
        Event mask
    :param cookie:
        Event cookie
    :param name:
        Base name of the event source path.
    :param src_path:
        Full event source path.
    """

    def __init__(self, wd, mask, cookie, name, src_path):
        self._wd = wd
        self._mask = mask
        self._cookie = cookie
        self._name = name
        self._src_path = src_path

    @property
    def src_path(self):
        return self._src_path

    @property
    def wd(self):
        return self._wd

    @property
    def mask(self):
        return self._mask

    @property
    def cookie(self):
        return self._cookie

    @property
    def name(self):
        return self._name

    @property
    def is_modify(self):
        return self._mask & InotifyConstants.IN_MODIFY > 0

    @property
    def is_close_write(self):
        return self._mask & InotifyConstants.IN_CLOSE_WRITE > 0

    @property
    def is_close_nowrite(self):
        return self._mask & InotifyConstants.IN_CLOSE_NOWRITE > 0

    @property
    def is_open(self):
        return self._mask & InotifyConstants.IN_OPEN > 0

    @property
    def is_access(self):
        return self._mask & InotifyConstants.IN_ACCESS > 0

    @property
    def is_delete(self):
        return self._mask & InotifyConstants.IN_DELETE > 0

    @property
    def is_delete_self(self):
        return self._mask & InotifyConstants.IN_DELETE_SELF > 0

    @property
    def is_create(self):
        return self._mask & InotifyConstants.IN_CREATE > 0

    @property
    def is_moved_from(self):
        return self._mask & InotifyConstants.IN_MOVED_FROM > 0

    @property
    def is_moved_to(self):
        return self._mask & InotifyConstants.IN_MOVED_TO > 0

    @property
    def is_move(self):
        return self._mask & InotifyConstants.IN_MOVE > 0

    @property
    def is_move_self(self):
        return self._mask & InotifyConstants.IN_MOVE_SELF > 0

    @property
    def is_attrib(self):
        return self._mask & InotifyConstants.IN_ATTRIB > 0

    @property
    def is_ignored(self):
        return self._mask & InotifyConstants.IN_IGNORED > 0

    @property
    def is_directory(self):
        # It looks like the kernel does not provide this information for
        # IN_DELETE_SELF and IN_MOVE_SELF. In this case, assume it's a dir.
        # See also: https://github.com/seb-m/pyinotify/blob/2c7e8f8/python2/pyinotify.py#L897
        return (
            self.is_delete_self
            or self.is_move_self
            or self._mask & InotifyConstants.IN_ISDIR > 0
        )

    @property
    def key(self):
        return self._src_path, self._wd, self._mask, self._cookie, self._name

    def __eq__(self, inotify_event):
        return self.key == inotify_event.key

    def __ne__(self, inotify_event):
        return self.key != inotify_event.key

    def __hash__(self):
        return hash(self.key)

    @staticmethod
    def _get_mask_string(mask):
        masks = []
        for c in dir(InotifyConstants):
            if c.startswith("IN_") and c not in [
                "IN_ALL_EVENTS",
                "IN_CLOSE",
                "IN_MOVE",
            ]:
                c_val = getattr(InotifyConstants, c)
                if mask & c_val:
                    masks.append(c)
        return "|".join(masks)

    def __repr__(self):
        return (
            f"<{type(self).__name__}: src_path={self.src_path!r}, wd={self.wd},"
            f" mask={self._get_mask_string(self.mask)}, cookie={self.cookie},"
            f" name={os.fsdecode(self.name)!r}>"
        )
