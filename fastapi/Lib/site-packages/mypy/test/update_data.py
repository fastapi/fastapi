from __future__ import annotations

import re
from collections import defaultdict
from typing import Iterator

from mypy.test.data import (
    DataDrivenTestCase,
    DataFileCollector,
    DataFileFix,
    parse_test_data,
)


def update_testcase_output(
    testcase: DataDrivenTestCase, actual: list[str], *, incremental_step: int
) -> None:
    if testcase.xfail:
        return
    collector = testcase.parent
    assert isinstance(collector, DataFileCollector)
    for fix in _iter_fixes(testcase, actual, incremental_step=incremental_step):
        collector.enqueue_fix(fix)


def _iter_fixes(
    testcase: DataDrivenTestCase, actual: list[str], *, incremental_step: int
) -> Iterator[DataFileFix]:
    reports_by_line: dict[tuple[str, int], list[tuple[str, str]]] = defaultdict(list)
    for error_line in actual:
        comment_match = re.match(
            r"^(?P<filename>[^:]+):(?P<lineno>\d+): (?P<severity>error|note|warning): (?P<msg>.+)$",
            error_line,
        )
        if comment_match:
            filename = comment_match.group("filename")
            lineno = int(comment_match.group("lineno"))
            severity = comment_match.group("severity")
            msg = comment_match.group("msg")
            reports_by_line[filename, lineno].append((severity, msg))

    test_items = parse_test_data(testcase.data, testcase.name)

    # If we have [out] and/or [outN], we update just those sections.
    if any(re.match(r"^out\d*$", test_item.id) for test_item in test_items):
        for test_item in test_items:
            if (incremental_step < 2 and test_item.id == "out") or (
                incremental_step >= 2 and test_item.id == f"out{incremental_step}"
            ):
                yield DataFileFix(
                    lineno=testcase.line + test_item.line - 1,
                    end_lineno=testcase.line + test_item.end_line - 1,
                    lines=actual + [""] * test_item.trimmed_newlines,
                )

        return

    # Update assertion comments within the sections
    for test_item in test_items:
        if test_item.id == "case":
            source_lines = test_item.data
            file_path = "main"
        elif test_item.id == "file":
            source_lines = test_item.data
            file_path = f"tmp/{test_item.arg}"
        else:
            continue  # other sections we don't touch

        fix_lines = []
        for lineno, source_line in enumerate(source_lines, start=1):
            reports = reports_by_line.get((file_path, lineno))
            comment_match = re.search(
                r"(?P<indent>\s+)(?P<comment># [EWN]: .+)$", source_line
            )
            if comment_match:
                source_line = source_line[
                    : comment_match.start("indent")
                ]  # strip old comment
            if reports:
                indent = comment_match.group("indent") if comment_match else "  "
                # multiline comments are on the first line and then on subsequent lines emtpy lines
                # with a continuation backslash
                for j, (severity, msg) in enumerate(reports):
                    out_l = source_line if j == 0 else " " * len(source_line)
                    is_last = j == len(reports) - 1
                    severity_char = severity[0].upper()
                    continuation = "" if is_last else " \\"
                    fix_lines.append(
                        f"{out_l}{indent}# {severity_char}: {msg}{continuation}"
                    )
            else:
                fix_lines.append(source_line)

        yield DataFileFix(
            lineno=testcase.line + test_item.line - 1,
            end_lineno=testcase.line + test_item.end_line - 1,
            lines=fix_lines + [""] * test_item.trimmed_newlines,
        )
