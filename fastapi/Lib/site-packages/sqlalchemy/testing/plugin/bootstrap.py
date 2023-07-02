"""
Bootstrapper for test framework plugins.

The entire rationale for this system is to get the modules in plugin/
imported without importing all of the supporting library, so that we can
set up things for testing before coverage starts.

The rationale for all of plugin/ being *in* the supporting library in the
first place is so that the testing and plugin suite is available to other
libraries, mainly external SQLAlchemy and Alembic dialects, to make use
of the same test environment and standard suites available to
SQLAlchemy/Alembic themselves without the need to ship/install a separate
package outside of SQLAlchemy.


"""

import os
import sys

bootstrap_file = locals()["bootstrap_file"]
to_bootstrap = locals()["to_bootstrap"]


def load_file_as_module(name):
    path = os.path.join(os.path.dirname(bootstrap_file), "%s.py" % name)

    if sys.version_info >= (3, 5):
        import importlib.util

        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None
        assert spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        import imp

        mod = imp.load_source(name, path)

    return mod


if to_bootstrap == "pytest":
    sys.modules["sqla_plugin_base"] = load_file_as_module("plugin_base")
    sys.modules["sqla_plugin_base"].bootstrapped_as_sqlalchemy = True
    if sys.version_info < (3, 0):
        sys.modules["sqla_reinvent_fixtures"] = load_file_as_module(
            "reinvent_fixtures_py2k"
        )
    sys.modules["sqla_pytestplugin"] = load_file_as_module("pytestplugin")
else:
    raise Exception("unknown bootstrap: %s" % to_bootstrap)  # noqa
