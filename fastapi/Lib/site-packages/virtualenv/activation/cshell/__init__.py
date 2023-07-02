from __future__ import annotations

from virtualenv.activation.via_template import ViaTemplateActivator


class CShellActivator(ViaTemplateActivator):
    @classmethod
    def supports(cls, interpreter):
        return interpreter.os != "nt"

    def templates(self):
        yield "activate.csh"


__all__ = [
    "CShellActivator",
]
