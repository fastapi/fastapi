"""A basic check to make sure that we are using a mypyc-compiled version when expected."""

from __future__ import annotations

import os
from unittest import TestCase

import mypy


class MypycTest(TestCase):
    def test_using_mypyc(self) -> None:
        if os.getenv("TEST_MYPYC", None) == "1":
            assert not mypy.__file__.endswith(
                ".py"
            ), "Expected to find a mypyc-compiled version"
