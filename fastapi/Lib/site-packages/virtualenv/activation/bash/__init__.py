from __future__ import annotations

from pathlib import Path

from virtualenv.activation.via_template import ViaTemplateActivator


class BashActivator(ViaTemplateActivator):
    def templates(self):
        yield "activate.sh"

    def as_name(self, template):
        return Path(template).stem


__all__ = [
    "BashActivator",
]
