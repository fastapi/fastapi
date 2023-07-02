from __future__ import annotations

import logging
import sys

LEVELS = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARNING,
    3: logging.INFO,
    4: logging.DEBUG,
    5: logging.NOTSET,
}

MAX_LEVEL = max(LEVELS.keys())
LOGGER = logging.getLogger()


def setup_report(verbosity, show_pid=False):  # noqa: FBT002
    _clean_handlers(LOGGER)
    if verbosity > MAX_LEVEL:
        verbosity = MAX_LEVEL  # pragma: no cover
    level = LEVELS[verbosity]
    msg_format = "%(message)s"
    if level <= logging.DEBUG:
        locate = "module"
        msg_format = (
            f"%(relativeCreated)d {msg_format} [%(levelname)s %({locate})s:%(lineno)d]"
        )
    if show_pid:
        msg_format = f"[%(process)d] {msg_format}"
    formatter = logging.Formatter(msg_format)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(level)
    LOGGER.setLevel(logging.NOTSET)
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(stream_handler)
    level_name = logging.getLevelName(level)
    logging.debug("setup logging to %s", level_name)
    logging.getLogger("distlib").setLevel(logging.ERROR)
    return verbosity


def _clean_handlers(log):
    for log_handler in list(log.handlers):  # remove handlers of libraries
        log.removeHandler(log_handler)


__all__ = [
    "LEVELS",
    "MAX_LEVEL",
    "setup_report",
]
