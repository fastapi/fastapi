from __future__ import annotations

from virtualenv.activation.via_template import ViaTemplateActivator


class FishActivator(ViaTemplateActivator):
    def templates(self):
        yield "activate.fish"


__all__ = [
    "FishActivator",
]
