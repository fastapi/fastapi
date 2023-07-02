"""Test exporting line-level reference information (undocumented feature)"""

from __future__ import annotations

import json
import os
import sys

from mypy import build
from mypy.modulefinder import BuildSource
from mypy.options import Options
from mypy.test.config import test_temp_dir
from mypy.test.data import DataDrivenTestCase, DataSuite
from mypy.test.helpers import assert_string_arrays_equal


class RefInfoSuite(DataSuite):
    required_out_section = True
    files = ["ref-info.test"]

    def run_case(self, testcase: DataDrivenTestCase) -> None:
        options = Options()
        options.use_builtins_fixtures = True
        options.show_traceback = True
        options.export_ref_info = True  # This is the flag we are testing

        src = "\n".join(testcase.input)
        result = build.build(
            sources=[BuildSource("main", None, src)],
            options=options,
            alt_lib_path=test_temp_dir,
        )
        assert not result.errors

        major, minor = sys.version_info[:2]
        ref_path = os.path.join(
            options.cache_dir, f"{major}.{minor}", "__main__.refs.json"
        )

        with open(ref_path) as refs_file:
            data = json.load(refs_file)

        a = []
        for item in data:
            a.append(f"{item['line']}:{item['column']}:{item['target']}")

        assert_string_arrays_equal(
            testcase.output,
            a,
            f"Invalid output ({testcase.file}, line {testcase.line})",
        )
