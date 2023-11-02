# Link checker script for https://github.com/tiangolo/fastapi
# Place it under fastapi/scripts or configure DOCS_ROOT below

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Generator

Line = str
LineNumber = int
Url = str
SearchResult = str
PatternSnippet = str
IfNotFiltered = bool
IfFilterMatches = bool
IfInCode = bool

# config

DOCS_ROOT = Path("../docs").resolve(strict=True)

# end config

CODE_EXAMPLES_REFERENCE_POINT = DOCS_ROOT / "en/docs"

NONEXISTING_TARGETS: set[Path] = set()
EXTERNAL_URLS: set[Url] = set()


@dataclass
class FileSearchResults:
    filepath: Path
    links: dict[LineNumber, list[tuple[Url, IfNotFiltered]]] = field(
        default_factory=dict
    )

    def __str__(self):
        result = ["    ", str(self.filepath), "\n"]
        for lnum, links in self.links.items():
            not_filtered = [match[0] for match in links if match[1]]
            if not_filtered:
                result.extend(
                    [
                        "    ",
                        "[",
                        str(lnum),
                        "] ",
                        ", ".join(not_filtered),
                        "\n",
                    ]
                )
        if len(result) > 3:
            return "".join(result)
        return ""


def iter_markdowns(path: Path) -> Generator[Path, Any, None]:
    for root, _, files in os.walk(path):
        root = Path(root)
        for file in files:
            if file.endswith(".md"):
                yield root / file


def iter_lines_and_context(
    filepath: Path,
) -> Generator[tuple[LineNumber, Line, IfInCode], Any, None]:
    with filepath.open("r", encoding="utf-8") as f:
        in_code = False
        for lnum, line in enumerate(f, start=1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            yield (lnum, line, in_code)


def iter_file_search_results(
    root: Path,
    ignore: list[Callable[[Url], IfFilterMatches]],
    linkpattern: re.Pattern[str] = re.compile(
        r"""
        \[ [^\]]* \]
        \(
            ( [^)]* )
        \)
        """,
        re.VERBOSE,
    ),
    in_code_linkpattern: re.Pattern[str] = re.compile(
        r"""
        [{]!> [^\S\n]*
        ( [\S]+?[.]py )
        [^\S\n]* ![}]
        """,
        re.VERBOSE,
    ),
) -> Generator[FileSearchResults, Any, None]:
    for filepath in iter_markdowns(root):
        results = FileSearchResults(filepath=filepath.resolve(strict=True))
        for lnum, line, in_code in iter_lines_and_context(filepath):
            pattern = in_code_linkpattern if in_code else linkpattern
            for match in pattern.finditer(line):
                link = match.group(1)
                check_target_exists(filepath, link, in_code)
                if lnum not in results.links:
                    line_results = []
                    results.links[lnum] = line_results
                line_results.append((link, True))  # type: ignore
        for filter in ignore:
            for links in results.links.values():
                for index, link in enumerate(links):
                    if link[1] and filter(link[0]):
                        links[index] = (link[0], False)
        if results.links:
            yield results


def check_target_exists(
    file: Path,
    url: Url,
    in_code: bool,
    without_hash_pattern: re.Pattern[str] = re.compile(
        r"""
        ^
        ( [^#]* )     # part before the hash
        (?: [#].* )?  # the hash
        $
        """,
        re.VERBOSE,
    ),
    lang_id_pattern: re.Pattern[str] = re.compile(
        r"""
        /[a-z]{2}/docs/  # matches the two digit language identifier
        """,
        re.VERBOSE,
    ),
):
    if in_code:
        reference_point = CODE_EXAMPLES_REFERENCE_POINT
        cleanurl = url
    else:
        if url.startswith("https://"):
            EXTERNAL_URLS.add(url)
            return
        reference_point = file.parent
        match = without_hash_pattern.match(url)
        if not match:
            raise Exception("could not match link, this should not happen")
        cleanurl = match.group(1)
        if not cleanurl:
            return
    joined = reference_point / cleanurl
    try:
        joined.resolve(strict=True)
    except FileNotFoundError:
        try:
            joined = Path(lang_id_pattern.sub("/en/docs/", str(joined))).resolve(
                strict=True
            )
        except FileNotFoundError:
            NONEXISTING_TARGETS.add(joined.resolve(strict=False))


@dataclass
class IsExternal:
    desc: str = "a https link to an external url"

    def __call__(self, url: Url):
        if url.startswith("https://"):
            return True
        return False


@dataclass
class IsWellFormed:
    desc: str = "a well-formed local relative link to a .md / .png / .py"

    word: PatternSnippet = r"""
    [a-z][a-z0-9]*
    (?:
        [-_]
        [a-z0-9]+
    )*
    """

    path: PatternSnippet = rf"""
    (?: [.][.]/ )* (?: {word}/ )*
    """

    filename: PatternSnippet = rf"""
    {word}[.](?: md|png|py )
    """

    hash: PatternSnippet = r"""
    (?: [#][^#]+ )
    """

    wellformed_pat: re.Pattern[str] = re.compile(
        rf"""
        ^
        (?:
            (?:
                {path}
                {filename}
                {hash}?
            )
            |
            {hash}
        )
        $
        """,
        re.VERBOSE,
    )

    def __call__(self, url: Url):
        if self.wellformed_pat.match(url):
            return True
        return False


if __name__ == "__main__":
    filters = [IsExternal(), IsWellFormed()]
    nasty_urls: list[SearchResult] = []
    for searchresult in iter_file_search_results(DOCS_ROOT, ignore=filters):
        searchresult = str(searchresult)
        if searchresult:
            nasty_urls.append(searchresult)
    if nasty_urls:
        print(f"\nThese links under {DOCS_ROOT} are not:\n")
        for filter in filters:
            print(f"* {filter.desc}")
        print()
        print("\n".join(nasty_urls))
    else:
        print(f"\nEach link under {DOCS_ROOT} is:\n")
        for filter in filters:
            print(f"* {filter.desc}")

    if NONEXISTING_TARGETS:
        print("\nThese files are referenced in links but do not exist:")
        for url in sorted(NONEXISTING_TARGETS):
            print(f"    {url}")
