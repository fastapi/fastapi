"""Ensure the argparse parser and Options class are in sync.

In particular, verify that the argparse defaults are the same as the Options
defaults, and that argparse doesn't assign any new members to the Options
object it creates.
"""
from __future__ import annotations

import argparse
import sys

from mypy.main import infer_python_executable, process_options
from mypy.options import Options
from mypy.test.helpers import Suite, assert_equal


class ArgSuite(Suite):
    def test_coherence(self) -> None:
        options = Options()
        _, parsed_options = process_options([], require_targets=False)
        # FIX: test this too. Requires changing working dir to avoid finding 'setup.cfg'
        options.config_file = parsed_options.config_file
        assert_equal(options.snapshot(), parsed_options.snapshot())

    def test_executable_inference(self) -> None:
        """Test the --python-executable flag with --python-version"""
        sys_ver_str = "{ver.major}.{ver.minor}".format(ver=sys.version_info)

        base = ["file.py"]  # dummy file

        # test inference given one (infer the other)
        matching_version = base + [f"--python-version={sys_ver_str}"]
        _, options = process_options(matching_version)
        assert options.python_version == sys.version_info[:2]
        assert options.python_executable == sys.executable

        matching_version = base + [f"--python-executable={sys.executable}"]
        _, options = process_options(matching_version)
        assert options.python_version == sys.version_info[:2]
        assert options.python_executable == sys.executable

        # test inference given both
        matching_version = base + [
            f"--python-version={sys_ver_str}",
            f"--python-executable={sys.executable}",
        ]
        _, options = process_options(matching_version)
        assert options.python_version == sys.version_info[:2]
        assert options.python_executable == sys.executable

        # test that --no-site-packages will disable executable inference
        matching_version = base + [
            f"--python-version={sys_ver_str}",
            "--no-site-packages",
        ]
        _, options = process_options(matching_version)
        assert options.python_version == sys.version_info[:2]
        assert options.python_executable is None

        # Test setting python_version/executable from config file
        special_opts = argparse.Namespace()
        special_opts.python_executable = None
        special_opts.python_version = None
        special_opts.no_executable = None

        # first test inferring executable from version
        options = Options()
        options.python_executable = None
        options.python_version = sys.version_info[:2]
        infer_python_executable(options, special_opts)
        assert options.python_version == sys.version_info[:2]
        assert options.python_executable == sys.executable

        # then test inferring version from executable
        options = Options()
        options.python_executable = sys.executable
        infer_python_executable(options, special_opts)
        assert options.python_version == sys.version_info[:2]
        assert options.python_executable == sys.executable
