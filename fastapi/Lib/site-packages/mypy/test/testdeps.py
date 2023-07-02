"""Test cases for generating node-level dependencies (for fine-grained incremental checking)"""

from __future__ import annotations

import os
from collections import defaultdict

from mypy import build
from mypy.errors import CompileError
from mypy.modulefinder import BuildSource
from mypy.nodes import Expression, MypyFile
from mypy.options import Options
from mypy.server.deps import get_dependencies
from mypy.test.config import test_temp_dir
from mypy.test.data import DataDrivenTestCase, DataSuite
from mypy.test.helpers import assert_string_arrays_equal, find_test_files, parse_options
from mypy.types import Type
from mypy.typestate import type_state

# Only dependencies in these modules are dumped
dumped_modules = ["__main__", "pkg", "pkg.mod"]


class GetDependenciesSuite(DataSuite):
    files = find_test_files(pattern="deps*.test")

    def run_case(self, testcase: DataDrivenTestCase) -> None:
        src = "\n".join(testcase.input)
        dump_all = "# __dump_all__" in src
        options = parse_options(src, testcase, incremental_step=1)
        options.use_builtins_fixtures = True
        options.show_traceback = True
        options.cache_dir = os.devnull
        options.export_types = True
        options.preserve_asts = True
        options.allow_empty_bodies = True
        messages, files, type_map = self.build(src, options)
        a = messages
        if files is None or type_map is None:
            if not a:
                a = [
                    "Unknown compile error (likely syntax error in test case or fixture)"
                ]
        else:
            deps: defaultdict[str, set[str]] = defaultdict(set)
            for module, file in files.items():
                if (module in dumped_modules or dump_all) and (
                    module in testcase.test_modules
                ):
                    new_deps = get_dependencies(
                        file, type_map, options.python_version, options
                    )
                    for source in new_deps:
                        deps[source].update(new_deps[source])

            type_state.add_all_protocol_deps(deps)

            for source, targets in sorted(deps.items()):
                if source.startswith(("<enum", "<typing", "<mypy", "<_typeshed.")):
                    # Remove noise.
                    continue
                line = f"{source} -> {', '.join(sorted(targets))}"
                # Clean up output a bit
                line = line.replace("__main__", "m")
                a.append(line)

        assert_string_arrays_equal(
            testcase.output,
            a,
            f"Invalid output ({testcase.file}, line {testcase.line})",
        )

    def build(
        self, source: str, options: Options
    ) -> tuple[list[str], dict[str, MypyFile] | None, dict[Expression, Type] | None]:
        try:
            result = build.build(
                sources=[BuildSource("main", None, source)],
                options=options,
                alt_lib_path=test_temp_dir,
            )
        except CompileError as e:
            # TODO: Should perhaps not return None here.
            return e.messages, None, None
        return result.errors, result.files, result.types
