"""Test cases for AST diff (used for fine-grained incremental checking)"""

from __future__ import annotations

import os

from mypy import build
from mypy.defaults import PYTHON3_VERSION
from mypy.errors import CompileError
from mypy.modulefinder import BuildSource
from mypy.nodes import MypyFile
from mypy.options import Options
from mypy.server.astdiff import compare_symbol_table_snapshots, snapshot_symbol_table
from mypy.test.config import test_temp_dir
from mypy.test.data import DataDrivenTestCase, DataSuite
from mypy.test.helpers import assert_string_arrays_equal, parse_options


class ASTDiffSuite(DataSuite):
    files = ["diff.test"]

    def run_case(self, testcase: DataDrivenTestCase) -> None:
        first_src = "\n".join(testcase.input)
        files_dict = dict(testcase.files)
        second_src = files_dict["tmp/next.py"]
        options = parse_options(first_src, testcase, 1)

        messages1, files1 = self.build(first_src, options)
        messages2, files2 = self.build(second_src, options)

        a = []
        if messages1:
            a.extend(messages1)
        if messages2:
            a.append("== next ==")
            a.extend(messages2)

        assert (
            files1 is not None and files2 is not None
        ), "cases where CompileError occurred should not be run"
        prefix = "__main__"
        snapshot1 = snapshot_symbol_table(prefix, files1["__main__"].names)
        snapshot2 = snapshot_symbol_table(prefix, files2["__main__"].names)
        diff = compare_symbol_table_snapshots(prefix, snapshot1, snapshot2)
        for trigger in sorted(diff):
            a.append(trigger)

        assert_string_arrays_equal(
            testcase.output,
            a,
            f"Invalid output ({testcase.file}, line {testcase.line})",
        )

    def build(
        self, source: str, options: Options
    ) -> tuple[list[str], dict[str, MypyFile] | None]:
        options.use_builtins_fixtures = True
        options.show_traceback = True
        options.cache_dir = os.devnull
        options.python_version = PYTHON3_VERSION
        options.allow_empty_bodies = True
        try:
            result = build.build(
                sources=[BuildSource("main", None, source)],
                options=options,
                alt_lib_path=test_temp_dir,
            )
        except CompileError as e:
            # TODO: Is it okay to return None?
            return e.messages, None
        return result.errors, result.files
