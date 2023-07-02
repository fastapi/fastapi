# testing/warnings.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

from __future__ import absolute_import

import warnings

from .. import exc as sa_exc
from ..util.langhelpers import _warnings_warn
from . import assertions


class SATestSuiteWarning(Warning):
    """warning for a condition detected during tests that is non-fatal

    Currently outside of SAWarning so that we can work around tools like
    Alembic doing the wrong thing with warnings.

    """


def warn_test_suite(message):
    _warnings_warn(message, category=SATestSuiteWarning)


def setup_filters():
    """Set global warning behavior for the test suite."""

    # TODO: at this point we can use the normal pytest warnings plugin,
    # if we decide the test suite can be linked to pytest only

    origin = r"^(?:test|sqlalchemy)\..*"

    warnings.filterwarnings("ignore", category=sa_exc.SAPendingDeprecationWarning)
    warnings.filterwarnings("error", category=sa_exc.SADeprecationWarning)
    warnings.filterwarnings("error", category=sa_exc.SAWarning)

    warnings.filterwarnings("always", category=SATestSuiteWarning)

    warnings.filterwarnings("error", category=DeprecationWarning, module=origin)

    # ignore things that are deprecated *as of* 2.0 :)
    warnings.filterwarnings(
        "ignore",
        category=sa_exc.SADeprecationWarning,
        message=r".*\(deprecated since: 2.0\)$",
    )
    warnings.filterwarnings(
        "ignore",
        category=sa_exc.SADeprecationWarning,
        message=r"^The (Sybase|firebird) dialect is deprecated and will be",
    )

    try:
        import pytest
    except ImportError:
        pass
    else:
        warnings.filterwarnings(
            "once", category=pytest.PytestDeprecationWarning, module=origin
        )


def assert_warnings(fn, warning_msgs, regex=False):
    """Assert that each of the given warnings are emitted by fn.

    Deprecated.  Please use assertions.expect_warnings().

    """

    with assertions._expect_warnings(sa_exc.SAWarning, warning_msgs, regex=regex):
        return fn()
