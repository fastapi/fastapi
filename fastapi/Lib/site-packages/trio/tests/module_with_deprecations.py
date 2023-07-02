regular = "hi"

from .. import _deprecate

_deprecate.enable_attribute_deprecations(__name__)

# Make sure that we don't trigger infinite recursion when accessing module
# attributes in between calling enable_attribute_deprecations and defining
# __deprecated_attributes__:
import sys

this_mod = sys.modules[__name__]
assert this_mod.regular == "hi"
assert not hasattr(this_mod, "dep1")

__deprecated_attributes__ = {
    "dep1": _deprecate.DeprecatedAttribute("value1", "1.1", issue=1),
    "dep2": _deprecate.DeprecatedAttribute(
        "value2", "1.2", issue=1, instead="instead-string"
    ),
}
