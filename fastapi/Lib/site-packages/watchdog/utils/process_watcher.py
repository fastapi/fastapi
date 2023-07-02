from __future__ import annotations

import logging

from watchdog.utils import BaseThread

logger = logging.getLogger(__name__)


class ProcessWatcher(BaseThread):
    def __init__(self, popen_obj, process_termination_callback):
        super().__init__()
        self.popen_obj = popen_obj
        self.process_termination_callback = process_termination_callback

    def run(self):
        while True:
            if self.popen_obj.poll() is not None:
                break
            if self.stopped_event.wait(timeout=0.1):
                return

        try:
            self.process_termination_callback()
        except Exception:
            logger.exception("Error calling process termination callback")
