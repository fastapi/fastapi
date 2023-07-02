from __future__ import annotations

from virtualenv.activation.via_template import ViaTemplateActivator


class NushellActivator(ViaTemplateActivator):
    def templates(self):
        yield "activate.nu"

    def replacements(self, creator, dest_folder):  # noqa: ARG002
        return {
            "__VIRTUAL_PROMPT__": "" if self.flag_prompt is None else self.flag_prompt,
            "__VIRTUAL_ENV__": str(creator.dest),
            "__VIRTUAL_NAME__": creator.env_name,
            "__BIN_NAME__": str(creator.bin_dir.relative_to(creator.dest)),
        }


__all__ = [
    "NushellActivator",
]
