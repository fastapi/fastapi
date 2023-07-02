# winapi.py: Windows API-Python interface (removes dependency on pywin32)
#
# Copyright (C) 2007 Thomas Heller <theller@ctypes.org>
# Copyright (C) 2010 Will McGugan <will@willmcgugan.com>
# Copyright (C) 2010 Ryan Kelly <ryan@rfk.id.au>
# Copyright (C) 2010 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright (C) 2014 Thomas Amland
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and / or other materials provided with the distribution.
# * Neither the name of the organization nor the names of its contributors may
#   be used to endorse or promote products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Portions of this code were taken from pyfilesystem, which uses the above
# new BSD license.

from __future__ import annotations

import sys
from functools import reduce

assert sys.platform.startswith("win"), f"{__name__} requires Windows"
import ctypes.wintypes  # noqa: E402

LPVOID = ctypes.wintypes.LPVOID

# Invalid handle value.
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

# File notification constants.
FILE_NOTIFY_CHANGE_FILE_NAME = 0x01
FILE_NOTIFY_CHANGE_DIR_NAME = 0x02
FILE_NOTIFY_CHANGE_ATTRIBUTES = 0x04
FILE_NOTIFY_CHANGE_SIZE = 0x08
FILE_NOTIFY_CHANGE_LAST_WRITE = 0x010
FILE_NOTIFY_CHANGE_LAST_ACCESS = 0x020
FILE_NOTIFY_CHANGE_CREATION = 0x040
FILE_NOTIFY_CHANGE_SECURITY = 0x0100

FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_OVERLAPPED = 0x40000000
FILE_LIST_DIRECTORY = 1
FILE_SHARE_READ = 0x01
FILE_SHARE_WRITE = 0x02
FILE_SHARE_DELETE = 0x04
OPEN_EXISTING = 3

VOLUME_NAME_NT = 0x02

# File action constants.
FILE_ACTION_CREATED = 1
FILE_ACTION_DELETED = 2
FILE_ACTION_MODIFIED = 3
FILE_ACTION_RENAMED_OLD_NAME = 4
FILE_ACTION_RENAMED_NEW_NAME = 5
FILE_ACTION_DELETED_SELF = 0xFFFE
FILE_ACTION_OVERFLOW = 0xFFFF

# Aliases
FILE_ACTION_ADDED = FILE_ACTION_CREATED
FILE_ACTION_REMOVED = FILE_ACTION_DELETED
FILE_ACTION_REMOVED_SELF = FILE_ACTION_DELETED_SELF

THREAD_TERMINATE = 0x0001

# IO waiting constants.
WAIT_ABANDONED = 0x00000080
WAIT_IO_COMPLETION = 0x000000C0
WAIT_OBJECT_0 = 0x00000000
WAIT_TIMEOUT = 0x00000102

# Error codes
ERROR_OPERATION_ABORTED = 995


class OVERLAPPED(ctypes.Structure):
    _fields_ = [
        ("Internal", LPVOID),
        ("InternalHigh", LPVOID),
        ("Offset", ctypes.wintypes.DWORD),
        ("OffsetHigh", ctypes.wintypes.DWORD),
        ("Pointer", LPVOID),
        ("hEvent", ctypes.wintypes.HANDLE),
    ]


def _errcheck_bool(value, func, args):
    if not value:
        raise ctypes.WinError()
    return args


def _errcheck_handle(value, func, args):
    if not value:
        raise ctypes.WinError()
    if value == INVALID_HANDLE_VALUE:
        raise ctypes.WinError()
    return args


def _errcheck_dword(value, func, args):
    if value == 0xFFFFFFFF:
        raise ctypes.WinError()
    return args


kernel32 = ctypes.WinDLL("kernel32")

ReadDirectoryChangesW = kernel32.ReadDirectoryChangesW
ReadDirectoryChangesW.restype = ctypes.wintypes.BOOL
ReadDirectoryChangesW.errcheck = _errcheck_bool
ReadDirectoryChangesW.argtypes = (
    ctypes.wintypes.HANDLE,  # hDirectory
    LPVOID,  # lpBuffer
    ctypes.wintypes.DWORD,  # nBufferLength
    ctypes.wintypes.BOOL,  # bWatchSubtree
    ctypes.wintypes.DWORD,  # dwNotifyFilter
    ctypes.POINTER(ctypes.wintypes.DWORD),  # lpBytesReturned
    ctypes.POINTER(OVERLAPPED),  # lpOverlapped
    LPVOID,  # FileIOCompletionRoutine # lpCompletionRoutine
)

CreateFileW = kernel32.CreateFileW
CreateFileW.restype = ctypes.wintypes.HANDLE
CreateFileW.errcheck = _errcheck_handle
CreateFileW.argtypes = (
    ctypes.wintypes.LPCWSTR,  # lpFileName
    ctypes.wintypes.DWORD,  # dwDesiredAccess
    ctypes.wintypes.DWORD,  # dwShareMode
    LPVOID,  # lpSecurityAttributes
    ctypes.wintypes.DWORD,  # dwCreationDisposition
    ctypes.wintypes.DWORD,  # dwFlagsAndAttributes
    ctypes.wintypes.HANDLE,  # hTemplateFile
)

CloseHandle = kernel32.CloseHandle
CloseHandle.restype = ctypes.wintypes.BOOL
CloseHandle.argtypes = (ctypes.wintypes.HANDLE,)  # hObject

CancelIoEx = kernel32.CancelIoEx
CancelIoEx.restype = ctypes.wintypes.BOOL
CancelIoEx.errcheck = _errcheck_bool
CancelIoEx.argtypes = (
    ctypes.wintypes.HANDLE,  # hObject
    ctypes.POINTER(OVERLAPPED),  # lpOverlapped
)

CreateEvent = kernel32.CreateEventW
CreateEvent.restype = ctypes.wintypes.HANDLE
CreateEvent.errcheck = _errcheck_handle
CreateEvent.argtypes = (
    LPVOID,  # lpEventAttributes
    ctypes.wintypes.BOOL,  # bManualReset
    ctypes.wintypes.BOOL,  # bInitialState
    ctypes.wintypes.LPCWSTR,  # lpName
)

SetEvent = kernel32.SetEvent
SetEvent.restype = ctypes.wintypes.BOOL
SetEvent.errcheck = _errcheck_bool
SetEvent.argtypes = (ctypes.wintypes.HANDLE,)  # hEvent

WaitForSingleObjectEx = kernel32.WaitForSingleObjectEx
WaitForSingleObjectEx.restype = ctypes.wintypes.DWORD
WaitForSingleObjectEx.errcheck = _errcheck_dword
WaitForSingleObjectEx.argtypes = (
    ctypes.wintypes.HANDLE,  # hObject
    ctypes.wintypes.DWORD,  # dwMilliseconds
    ctypes.wintypes.BOOL,  # bAlertable
)

CreateIoCompletionPort = kernel32.CreateIoCompletionPort
CreateIoCompletionPort.restype = ctypes.wintypes.HANDLE
CreateIoCompletionPort.errcheck = _errcheck_handle
CreateIoCompletionPort.argtypes = (
    ctypes.wintypes.HANDLE,  # FileHandle
    ctypes.wintypes.HANDLE,  # ExistingCompletionPort
    LPVOID,  # CompletionKey
    ctypes.wintypes.DWORD,  # NumberOfConcurrentThreads
)

GetQueuedCompletionStatus = kernel32.GetQueuedCompletionStatus
GetQueuedCompletionStatus.restype = ctypes.wintypes.BOOL
GetQueuedCompletionStatus.errcheck = _errcheck_bool
GetQueuedCompletionStatus.argtypes = (
    ctypes.wintypes.HANDLE,  # CompletionPort
    LPVOID,  # lpNumberOfBytesTransferred
    LPVOID,  # lpCompletionKey
    ctypes.POINTER(OVERLAPPED),  # lpOverlapped
    ctypes.wintypes.DWORD,  # dwMilliseconds
)

PostQueuedCompletionStatus = kernel32.PostQueuedCompletionStatus
PostQueuedCompletionStatus.restype = ctypes.wintypes.BOOL
PostQueuedCompletionStatus.errcheck = _errcheck_bool
PostQueuedCompletionStatus.argtypes = (
    ctypes.wintypes.HANDLE,  # CompletionPort
    ctypes.wintypes.DWORD,  # lpNumberOfBytesTransferred
    ctypes.wintypes.DWORD,  # lpCompletionKey
    ctypes.POINTER(OVERLAPPED),  # lpOverlapped
)


GetFinalPathNameByHandleW = kernel32.GetFinalPathNameByHandleW
GetFinalPathNameByHandleW.restype = ctypes.wintypes.DWORD
GetFinalPathNameByHandleW.errcheck = _errcheck_dword
GetFinalPathNameByHandleW.argtypes = (
    ctypes.wintypes.HANDLE,  # hFile
    ctypes.wintypes.LPWSTR,  # lpszFilePath
    ctypes.wintypes.DWORD,  # cchFilePath
    ctypes.wintypes.DWORD,  # DWORD
)


class FILE_NOTIFY_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("NextEntryOffset", ctypes.wintypes.DWORD),
        ("Action", ctypes.wintypes.DWORD),
        ("FileNameLength", ctypes.wintypes.DWORD),
        # ("FileName", (ctypes.wintypes.WCHAR * 1))]
        ("FileName", (ctypes.c_char * 1)),
    ]


LPFNI = ctypes.POINTER(FILE_NOTIFY_INFORMATION)


# We don't need to recalculate these flags every time a call is made to
# the win32 API functions.
WATCHDOG_FILE_FLAGS = FILE_FLAG_BACKUP_SEMANTICS
WATCHDOG_FILE_SHARE_FLAGS = reduce(
    lambda x, y: x | y,
    [
        FILE_SHARE_READ,
        FILE_SHARE_WRITE,
        FILE_SHARE_DELETE,
    ],
)
WATCHDOG_FILE_NOTIFY_FLAGS = reduce(
    lambda x, y: x | y,
    [
        FILE_NOTIFY_CHANGE_FILE_NAME,
        FILE_NOTIFY_CHANGE_DIR_NAME,
        FILE_NOTIFY_CHANGE_ATTRIBUTES,
        FILE_NOTIFY_CHANGE_SIZE,
        FILE_NOTIFY_CHANGE_LAST_WRITE,
        FILE_NOTIFY_CHANGE_SECURITY,
        FILE_NOTIFY_CHANGE_LAST_ACCESS,
        FILE_NOTIFY_CHANGE_CREATION,
    ],
)

# ReadDirectoryChangesW buffer length.
# To handle cases with lot of changes, this seems the highest safest value we can use.
# Note: it will fail with ERROR_INVALID_PARAMETER when it is greater than 64 KB and
#       the application is monitoring a directory over the network.
#       This is due to a packet size limitation with the underlying file sharing protocols.
#       https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-readdirectorychangesw#remarks
BUFFER_SIZE = 64000

# Buffer length for path-related stuff.
# Introduced to keep the old behavior when we bumped BUFFER_SIZE from 2048 to 64000 in v1.0.0.
PATH_BUFFER_SIZE = 2048


def _parse_event_buffer(readBuffer, nBytes):
    results = []
    while nBytes > 0:
        fni = ctypes.cast(readBuffer, LPFNI)[0]
        ptr = ctypes.addressof(fni) + FILE_NOTIFY_INFORMATION.FileName.offset
        # filename = ctypes.wstring_at(ptr, fni.FileNameLength)
        filename = ctypes.string_at(ptr, fni.FileNameLength)
        results.append((fni.Action, filename.decode("utf-16")))
        numToSkip = fni.NextEntryOffset
        if numToSkip <= 0:
            break
        readBuffer = readBuffer[numToSkip:]
        nBytes -= numToSkip  # numToSkip is long. nBytes should be long too.
    return results


def _is_observed_path_deleted(handle, path):
    # Comparison of observed path and actual path, returned by
    # GetFinalPathNameByHandleW. If directory moved to the trash bin, or
    # deleted, actual path will not be equal to observed path.
    buff = ctypes.create_unicode_buffer(PATH_BUFFER_SIZE)
    GetFinalPathNameByHandleW(handle, buff, PATH_BUFFER_SIZE, VOLUME_NAME_NT)
    return buff.value != path


def _generate_observed_path_deleted_event():
    # Create synthetic event for notify that observed directory is deleted
    path = ctypes.create_unicode_buffer(".")
    event = FILE_NOTIFY_INFORMATION(
        0, FILE_ACTION_DELETED_SELF, len(path), path.value.encode("utf-8")
    )
    event_size = ctypes.sizeof(event)
    buff = ctypes.create_string_buffer(PATH_BUFFER_SIZE)
    ctypes.memmove(buff, ctypes.addressof(event), event_size)
    return buff, event_size


def get_directory_handle(path):
    """Returns a Windows handle to the specified directory path."""
    return CreateFileW(
        path,
        FILE_LIST_DIRECTORY,
        WATCHDOG_FILE_SHARE_FLAGS,
        None,
        OPEN_EXISTING,
        WATCHDOG_FILE_FLAGS,
        None,
    )


def close_directory_handle(handle):
    try:
        CancelIoEx(handle, None)  # force ReadDirectoryChangesW to return
        CloseHandle(handle)  # close directory handle
    except OSError:
        try:
            CloseHandle(handle)  # close directory handle
        except Exception:
            return


def read_directory_changes(handle, path, recursive):
    """Read changes to the directory using the specified directory handle.

    http://timgolden.me.uk/pywin32-docs/win32file__ReadDirectoryChangesW_meth.html
    """
    event_buffer = ctypes.create_string_buffer(BUFFER_SIZE)
    nbytes = ctypes.wintypes.DWORD()
    try:
        ReadDirectoryChangesW(
            handle,
            ctypes.byref(event_buffer),
            len(event_buffer),
            recursive,
            WATCHDOG_FILE_NOTIFY_FLAGS,
            ctypes.byref(nbytes),
            None,
            None,
        )
    except OSError as e:
        if e.winerror == ERROR_OPERATION_ABORTED:
            return [], 0

        # Handle the case when the root path is deleted
        if _is_observed_path_deleted(handle, path):
            return _generate_observed_path_deleted_event()

        raise e

    return event_buffer.raw, int(nbytes.value)


class WinAPINativeEvent:
    def __init__(self, action, src_path):
        self.action = action
        self.src_path = src_path

    @property
    def is_added(self):
        return self.action == FILE_ACTION_CREATED

    @property
    def is_removed(self):
        return self.action == FILE_ACTION_REMOVED

    @property
    def is_modified(self):
        return self.action == FILE_ACTION_MODIFIED

    @property
    def is_renamed_old(self):
        return self.action == FILE_ACTION_RENAMED_OLD_NAME

    @property
    def is_renamed_new(self):
        return self.action == FILE_ACTION_RENAMED_NEW_NAME

    @property
    def is_removed_self(self):
        return self.action == FILE_ACTION_REMOVED_SELF

    def __repr__(self):
        return (
            f"<{type(self).__name__}: action={self.action}, src_path={self.src_path!r}>"
        )


def read_events(handle, path, recursive):
    buf, nbytes = read_directory_changes(handle, path, recursive)
    events = _parse_event_buffer(buf, nbytes)
    return [WinAPINativeEvent(action, src_path) for action, src_path in events]
