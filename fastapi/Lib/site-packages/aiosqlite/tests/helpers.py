# Copyright 2022 Amethyst Reese
# Licensed under the MIT license

import logging
import sys


def setup_logger():
    log = logging.getLogger("")
    log.setLevel(logging.INFO)

    logging.addLevelName(logging.ERROR, "E")
    logging.addLevelName(logging.WARNING, "W")
    logging.addLevelName(logging.INFO, "I")
    logging.addLevelName(logging.DEBUG, "V")

    date_fmt = r"%H:%M:%S"
    verbose_fmt = (
        "%(asctime)s,%(msecs)d %(levelname)s "
        "%(module)s:%(funcName)s():%(lineno)d   "
        "%(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(verbose_fmt, date_fmt))
    log.addHandler(handler)

    return log
