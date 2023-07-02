from __future__ import annotations

import os
from collections import OrderedDict

from virtualenv.activation.via_template import ViaTemplateActivator


class PythonActivator(ViaTemplateActivator):
    def templates(self):
        yield "activate_this.py"

    def replacements(self, creator, dest_folder):
        replacements = super().replacements(creator, dest_folder)
        lib_folders = OrderedDict(
            (os.path.relpath(str(i), str(dest_folder)), None) for i in creator.libs
        )
        lib_folders = os.pathsep.join(lib_folders.keys()).replace(
            "\\", "\\\\"
        )  # escape Windows path characters
        replacements.update(
            {
                "__LIB_FOLDERS__": lib_folders,
                "__DECODE_PATH__": "",
            },
        )
        return replacements


__all__ = [
    "PythonActivator",
]
