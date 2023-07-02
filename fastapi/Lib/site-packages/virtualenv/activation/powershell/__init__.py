from __future__ import annotations

from virtualenv.activation.via_template import ViaTemplateActivator


class PowerShellActivator(ViaTemplateActivator):
    def templates(self):
        yield "activate.ps1"


__all__ = [
    "PowerShellActivator",
]
