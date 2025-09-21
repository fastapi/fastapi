import warnings

import pydantic

try:
    from pydantic_extra_types.color import Color
except ImportError:
    from pydantic.color import Color  # triggers DeprecationWarning on v1


class Model(pydantic.BaseModel):
    c: Color


def test_color_deprecation_warning():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        m = Model(c="#FF0000")
        dep_warnings = [
            warn for warn in w if issubclass(warn.category, DeprecationWarning)
        ]
        assert len(dep_warnings) == 0, "DeprecationWarning raised! Fixed in this PR"
