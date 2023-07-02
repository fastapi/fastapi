from __future__ import annotations

import sys
from io import StringIO

import mypy.api
from mypy.test.helpers import Suite


class APISuite(Suite):
    def setUp(self) -> None:
        self.sys_stdout = sys.stdout
        self.sys_stderr = sys.stderr
        sys.stdout = self.stdout = StringIO()
        sys.stderr = self.stderr = StringIO()

    def tearDown(self) -> None:
        sys.stdout = self.sys_stdout
        sys.stderr = self.sys_stderr
        assert self.stdout.getvalue() == ""
        assert self.stderr.getvalue() == ""

    def test_capture_bad_opt(self) -> None:
        """stderr should be captured when a bad option is passed."""
        _, stderr, _ = mypy.api.run(["--some-bad-option"])
        assert isinstance(stderr, str)
        assert stderr != ""

    def test_capture_empty(self) -> None:
        """stderr should be captured when a bad option is passed."""
        _, stderr, _ = mypy.api.run([])
        assert isinstance(stderr, str)
        assert stderr != ""

    def test_capture_help(self) -> None:
        """stdout should be captured when --help is passed."""
        stdout, _, _ = mypy.api.run(["--help"])
        assert isinstance(stdout, str)
        assert stdout != ""

    def test_capture_version(self) -> None:
        """stdout should be captured when --version is passed."""
        stdout, _, _ = mypy.api.run(["--version"])
        assert isinstance(stdout, str)
        assert stdout != ""
