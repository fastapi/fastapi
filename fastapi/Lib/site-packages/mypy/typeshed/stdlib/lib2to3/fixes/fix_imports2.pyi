from . import fix_imports

MAPPING: dict[str, str]

class FixImports2(fix_imports.FixImports):
    mapping = MAPPING
