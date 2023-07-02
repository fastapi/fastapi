from __future__ import annotations

from io import BytesIO
from os import PathLike
from subprocess import DEVNULL, PIPE, CalledProcessError, CompletedProcess
from typing import (
    IO,
    Any,
    AsyncIterable,
    Mapping,
    Sequence,
    cast,
)

from ..abc import Process
from ._eventloop import get_asynclib
from ._tasks import create_task_group


async def run_process(
    command: str | bytes | Sequence[str | bytes],
    *,
    input: bytes | None = None,
    stdout: int | IO[Any] | None = PIPE,
    stderr: int | IO[Any] | None = PIPE,
    check: bool = True,
    cwd: str | bytes | PathLike[str] | None = None,
    env: Mapping[str, str] | None = None,
    start_new_session: bool = False,
) -> CompletedProcess[bytes]:
    """
    Run an external command in a subprocess and wait until it completes.

    .. seealso:: :func:`subprocess.run`

    :param command: either a string to pass to the shell, or an iterable of strings containing the
        executable name or path and its arguments
    :param input: bytes passed to the standard input of the subprocess
    :param stdout: either :data:`subprocess.PIPE` or :data:`subprocess.DEVNULL`
    :param stderr: one of :data:`subprocess.PIPE`, :data:`subprocess.DEVNULL` or
        :data:`subprocess.STDOUT`
    :param check: if ``True``, raise :exc:`~subprocess.CalledProcessError` if the process
        terminates with a return code other than 0
    :param cwd: If not ``None``, change the working directory to this before running the command
    :param env: if not ``None``, this mapping replaces the inherited environment variables from the
        parent process
    :param start_new_session: if ``true`` the setsid() system call will be made in the child
        process prior to the execution of the subprocess. (POSIX only)
    :return: an object representing the completed process
    :raises ~subprocess.CalledProcessError: if ``check`` is ``True`` and the process exits with a
        nonzero return code

    """

    async def drain_stream(stream: AsyncIterable[bytes], index: int) -> None:
        buffer = BytesIO()
        async for chunk in stream:
            buffer.write(chunk)

        stream_contents[index] = buffer.getvalue()

    async with await open_process(
        command,
        stdin=PIPE if input else DEVNULL,
        stdout=stdout,
        stderr=stderr,
        cwd=cwd,
        env=env,
        start_new_session=start_new_session,
    ) as process:
        stream_contents: list[bytes | None] = [None, None]
        try:
            async with create_task_group() as tg:
                if process.stdout:
                    tg.start_soon(drain_stream, process.stdout, 0)
                if process.stderr:
                    tg.start_soon(drain_stream, process.stderr, 1)
                if process.stdin and input:
                    await process.stdin.send(input)
                    await process.stdin.aclose()

                await process.wait()
        except BaseException:
            process.kill()
            raise

    output, errors = stream_contents
    if check and process.returncode != 0:
        raise CalledProcessError(cast(int, process.returncode), command, output, errors)

    return CompletedProcess(command, cast(int, process.returncode), output, errors)


async def open_process(
    command: str | bytes | Sequence[str | bytes],
    *,
    stdin: int | IO[Any] | None = PIPE,
    stdout: int | IO[Any] | None = PIPE,
    stderr: int | IO[Any] | None = PIPE,
    cwd: str | bytes | PathLike[str] | None = None,
    env: Mapping[str, str] | None = None,
    start_new_session: bool = False,
) -> Process:
    """
    Start an external command in a subprocess.

    .. seealso:: :class:`subprocess.Popen`

    :param command: either a string to pass to the shell, or an iterable of strings containing the
        executable name or path and its arguments
    :param stdin: one of :data:`subprocess.PIPE`, :data:`subprocess.DEVNULL`, a
        file-like object, or ``None``
    :param stdout: one of :data:`subprocess.PIPE`, :data:`subprocess.DEVNULL`,
        a file-like object, or ``None``
    :param stderr: one of :data:`subprocess.PIPE`, :data:`subprocess.DEVNULL`,
        :data:`subprocess.STDOUT`, a file-like object, or ``None``
    :param cwd: If not ``None``, the working directory is changed before executing
    :param env: If env is not ``None``, it must be a mapping that defines the environment
        variables for the new process
    :param start_new_session: if ``true`` the setsid() system call will be made in the child
        process prior to the execution of the subprocess. (POSIX only)
    :return: an asynchronous process object

    """
    shell = isinstance(command, str)
    return await get_asynclib().open_process(
        command,
        shell=shell,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        cwd=cwd,
        env=env,
        start_new_session=start_new_session,
    )
