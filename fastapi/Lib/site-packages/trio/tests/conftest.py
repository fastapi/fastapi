# XX this does not belong here -- b/c it's here, these things only apply to
# the tests in trio/_core/tests, not in trio/tests. For now there's some
# copy-paste...
#
# this stuff should become a proper pytest plugin

import inspect

import pytest

from ..testing import MockClock, trio_test

RUN_SLOW = True


def pytest_addoption(parser):
    parser.addoption("--run-slow", action="store_true", help="run slow tests")


def pytest_configure(config):
    global RUN_SLOW
    RUN_SLOW = config.getoption("--run-slow", True)


@pytest.fixture
def mock_clock():
    return MockClock()


@pytest.fixture
def autojump_clock():
    return MockClock(autojump_threshold=0)


# FIXME: split off into a package (or just make part of Trio's public
# interface?), with config file to enable? and I guess a mark option too; I
# guess it's useful with the class- and file-level marking machinery (where
# the raw @trio_test decorator isn't enough).
@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    if inspect.iscoroutinefunction(pyfuncitem.obj):
        pyfuncitem.obj = trio_test(pyfuncitem.obj)
