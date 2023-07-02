"""The Apple Framework builds require their own customization."""
from __future__ import annotations

import logging
import os
import struct
import subprocess
from abc import ABCMeta, abstractmethod
from pathlib import Path
from textwrap import dedent

from virtualenv.create.via_global_ref.builtin.ref import (
    ExePathRefToDest,
    PathRefToDest,
    RefMust,
)

from .common import CPython, CPythonPosix, is_mac_os_framework
from .cpython3 import CPython3


class CPythonmacOsFramework(CPython, metaclass=ABCMeta):
    @classmethod
    def can_describe(cls, interpreter):
        return is_mac_os_framework(interpreter) and super().can_describe(interpreter)

    def create(self):
        super().create()

        # change the install_name of the copied python executables
        target = self.desired_mach_o_image_path()
        current = self.current_mach_o_image_path()
        for src in self._sources:
            if isinstance(src, ExePathRefToDest) and (
                src.must == RefMust.COPY or not self.symlinks
            ):
                exes = [self.bin_dir / src.base]
                if not self.symlinks:
                    exes.extend(self.bin_dir / a for a in src.aliases)
                for exe in exes:
                    fix_mach_o(str(exe), current, target, self.interpreter.max_size)

    @classmethod
    def _executables(cls, interpreter):
        for _, targets, must, when in super()._executables(interpreter):
            # Make sure we use the embedded interpreter inside the framework, even if sys.executable points to the
            # stub executable in ${sys.prefix}/bin.
            # See http://groups.google.com/group/python-virtualenv/browse_thread/thread/17cab2f85da75951
            fixed_host_exe = (
                Path(interpreter.prefix)
                / "Resources"
                / "Python.app"
                / "Contents"
                / "MacOS"
                / "Python"
            )
            yield fixed_host_exe, targets, must, when

    @abstractmethod
    def current_mach_o_image_path(self):
        raise NotImplementedError

    @abstractmethod
    def desired_mach_o_image_path(self):
        raise NotImplementedError


class CPython3macOsFramework(CPythonmacOsFramework, CPython3, CPythonPosix):
    def current_mach_o_image_path(self):
        return "@executable_path/../../../../Python3"

    def desired_mach_o_image_path(self):
        return "@executable_path/../.Python"

    @classmethod
    def sources(cls, interpreter):
        yield from super().sources(interpreter)

        # add a symlink to the host python image
        exe = Path(interpreter.prefix) / "Python3"
        yield PathRefToDest(
            exe, dest=lambda self, _: self.dest / ".Python", must=RefMust.SYMLINK
        )

    @property
    def reload_code(self):
        result = super().reload_code
        result = dedent(
            f"""
        # the bundled site.py always adds the global site package if we're on python framework build, escape this
        import sys
        before = sys._framework
        try:
            sys._framework = None
            {result}
        finally:
            sys._framework = before
        """,
        )
        return result


def fix_mach_o(exe, current, new, max_size):
    """
    https://en.wikipedia.org/wiki/Mach-O.

    Mach-O, short for Mach object file format, is a file format for executables, object code, shared libraries,
    dynamically-loaded code, and core dumps. A replacement for the a.out format, Mach-O offers more extensibility and
    faster access to information in the symbol table.

    Each Mach-O file is made up of one Mach-O header, followed by a series of load commands, followed by one or more
    segments, each of which contains between 0 and 255 sections. Mach-O uses the REL relocation format to handle
    references to symbols. When looking up symbols Mach-O uses a two-level namespace that encodes each symbol into an
    'object/symbol name' pair that is then linearly searched for by first the object and then the symbol name.

    The basic structure—a list of variable-length "load commands" that reference pages of data elsewhere in the file—was
    also used in the executable file format for Accent. The Accent file format was in turn, based on an idea from Spice
    Lisp.

    With the introduction of Mac OS X 10.6 platform the Mach-O file underwent a significant modification that causes
    binaries compiled on a computer running 10.6 or later to be (by default) executable only on computers running Mac
    OS X 10.6 or later. The difference stems from load commands that the dynamic linker, in previous Mac OS X versions,
    does not understand. Another significant change to the Mach-O format is the change in how the Link Edit tables
    (found in the __LINKEDIT section) function. In 10.6 these new Link Edit tables are compressed by removing unused and
    unneeded bits of information, however Mac OS X 10.5 and earlier cannot read this new Link Edit table format.
    """
    try:
        logging.debug("change Mach-O for %s from %s to %s", exe, current, new)
        _builtin_change_mach_o(max_size)(exe, current, new)
    except Exception as e:  # noqa: BLE001
        logging.warning(
            "Could not call _builtin_change_mac_o: %s. Trying to call install_name_tool instead.",
            e,
        )
        try:
            cmd = ["install_name_tool", "-change", current, new, exe]
            subprocess.check_call(cmd)  # noqa: S603
        except Exception:
            logging.fatal(
                "Could not call install_name_tool -- you must have Apple's development tools installed"
            )
            raise


def _builtin_change_mach_o(maxint):  # noqa: C901
    MH_MAGIC = 0xFEEDFACE  # noqa: N806
    MH_CIGAM = 0xCEFAEDFE  # noqa: N806
    MH_MAGIC_64 = 0xFEEDFACF  # noqa: N806
    MH_CIGAM_64 = 0xCFFAEDFE  # noqa: N806
    FAT_MAGIC = 0xCAFEBABE  # noqa: N806
    BIG_ENDIAN = ">"  # noqa: N806
    LITTLE_ENDIAN = "<"  # noqa: N806
    LC_LOAD_DYLIB = 0xC  # noqa: N806

    class FileView:
        """A proxy for file-like objects that exposes a given view of a file. Modified from macholib."""

        def __init__(self, file_obj, start=0, size=maxint) -> None:
            if isinstance(file_obj, FileView):
                self._file_obj = file_obj._file_obj  # noqa: SLF001
            else:
                self._file_obj = file_obj
            self._start = start
            self._end = start + size
            self._pos = 0

        def __repr__(self) -> str:
            return f"<fileview [{self._start:d}, {self._end:d}] {self._file_obj!r}>"

        def tell(self):
            return self._pos

        def _checkwindow(self, seek_to, op):
            if not (self._start <= seek_to <= self._end):
                msg = f"{op} to offset {seek_to:d} is outside window [{self._start:d}, {self._end:d}]"
                raise OSError(msg)

        def seek(self, offset, whence=0):
            seek_to = offset
            if whence == os.SEEK_SET:
                seek_to += self._start
            elif whence == os.SEEK_CUR:
                seek_to += self._start + self._pos
            elif whence == os.SEEK_END:
                seek_to += self._end
            else:
                msg = f"Invalid whence argument to seek: {whence!r}"
                raise OSError(msg)
            self._checkwindow(seek_to, "seek")
            self._file_obj.seek(seek_to)
            self._pos = seek_to - self._start

        def write(self, content):
            here = self._start + self._pos
            self._checkwindow(here, "write")
            self._checkwindow(here + len(content), "write")
            self._file_obj.seek(here, os.SEEK_SET)
            self._file_obj.write(content)
            self._pos += len(content)

        def read(self, size=maxint):
            assert size >= 0  # noqa: S101
            here = self._start + self._pos
            self._checkwindow(here, "read")
            size = min(size, self._end - here)
            self._file_obj.seek(here, os.SEEK_SET)
            read_bytes = self._file_obj.read(size)
            self._pos += len(read_bytes)
            return read_bytes

    def read_data(file, endian, num=1):
        """Read a given number of 32-bits unsigned integers from the given file with the given endianness."""
        res = struct.unpack(endian + "L" * num, file.read(num * 4))
        if len(res) == 1:
            return res[0]
        return res

    def mach_o_change(at_path, what, value):  # noqa: C901
        """
        Replace a given name (what) in any LC_LOAD_DYLIB command found in the given binary with a new name (value),
        provided it's shorter.
        """  # noqa: D205

        def do_macho(file, bits, endian):
            # Read Mach-O header (the magic number is assumed read by the caller)
            (
                cpu_type,
                cpu_sub_type,
                file_type,
                n_commands,
                size_of_commands,
                flags,
            ) = read_data(file, endian, 6)
            # 64-bits header has one more field.
            if bits == 64:  # noqa: PLR2004
                read_data(file, endian)
            # The header is followed by n commands
            for _ in range(n_commands):
                where = file.tell()
                # Read command header
                cmd, cmd_size = read_data(file, endian, 2)
                if cmd == LC_LOAD_DYLIB:
                    # The first data field in LC_LOAD_DYLIB commands is the offset of the name, starting from the
                    # beginning of the  command.
                    name_offset = read_data(file, endian)
                    file.seek(where + name_offset, os.SEEK_SET)
                    # Read the NUL terminated string
                    load = file.read(cmd_size - name_offset).decode()
                    load = load[: load.index("\0")]
                    # If the string is what is being replaced, overwrite it.
                    if load == what:
                        file.seek(where + name_offset, os.SEEK_SET)
                        file.write(value.encode() + b"\0")
                # Seek to the next command
                file.seek(where + cmd_size, os.SEEK_SET)

        def do_file(file, offset=0, size=maxint):
            file = FileView(file, offset, size)
            # Read magic number
            magic = read_data(file, BIG_ENDIAN)
            if magic == FAT_MAGIC:
                # Fat binaries contain nfat_arch Mach-O binaries
                n_fat_arch = read_data(file, BIG_ENDIAN)
                for _ in range(n_fat_arch):
                    # Read arch header
                    cpu_type, cpu_sub_type, offset, size, align = read_data(
                        file, BIG_ENDIAN, 5
                    )
                    do_file(file, offset, size)
            elif magic == MH_MAGIC:
                do_macho(file, 32, BIG_ENDIAN)
            elif magic == MH_CIGAM:
                do_macho(file, 32, LITTLE_ENDIAN)
            elif magic == MH_MAGIC_64:
                do_macho(file, 64, BIG_ENDIAN)
            elif magic == MH_CIGAM_64:
                do_macho(file, 64, LITTLE_ENDIAN)

        assert len(what) >= len(value)  # noqa: S101

        with open(at_path, "r+b") as f:
            do_file(f)

    return mach_o_change


__all__ = [
    "CPythonmacOsFramework",
    "CPython3macOsFramework",
]
