"""Identity AST transform test cases"""

from __future__ import annotations

from mypy import build
from mypy.errors import CompileError
from mypy.modulefinder import BuildSource
from mypy.options import TYPE_VAR_TUPLE, UNPACK
from mypy.test.config import test_temp_dir
from mypy.test.data import DataDrivenTestCase, DataSuite
from mypy.test.helpers import (
    assert_string_arrays_equal,
    normalize_error_messages,
    parse_options,
)
from mypy.test.visitors import TypeAssertTransformVisitor


class TransformSuite(DataSuite):
    required_out_section = True
    # Reuse semantic analysis test cases.
    files = [
        "semanal-basic.test",
        "semanal-expressions.test",
        "semanal-classes.test",
        "semanal-types.test",
        "semanal-modules.test",
        "semanal-statements.test",
        "semanal-abstractclasses.test",
    ]
    native_sep = True

    def run_case(self, testcase: DataDrivenTestCase) -> None:
        test_transform(testcase)


def test_transform(testcase: DataDrivenTestCase) -> None:
    """Perform an identity transform test case."""

    try:
        src = "\n".join(testcase.input)
        options = parse_options(src, testcase, 1)
        options.use_builtins_fixtures = True
        options.semantic_analysis_only = True
        options.enable_incomplete_feature = [TYPE_VAR_TUPLE, UNPACK]
        options.show_traceback = True
        options.force_uppercase_builtins = True
        result = build.build(
            sources=[BuildSource("main", None, src)],
            options=options,
            alt_lib_path=test_temp_dir,
        )
        a = result.errors
        if a:
            raise CompileError(a)
        # Include string representations of the source files in the actual
        # output.
        for module in sorted(result.files.keys()):
            if module in testcase.test_modules:
                t = TypeAssertTransformVisitor()
                t.test_only = True
                file = t.mypyfile(result.files[module])
                a += file.str_with_options(options).split("\n")
    except CompileError as e:
        a = e.messages
    if testcase.normalize_output:
        a = normalize_error_messages(a)
    assert_string_arrays_equal(
        testcase.output,
        a,
        f"Invalid semantic analyzer output ({testcase.file}, line {testcase.line})",
    )
