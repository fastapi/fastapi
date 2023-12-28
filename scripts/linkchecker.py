from __future__ import annotations
from pathlib import Path
import os
from pprint import pprint as pp  # type: ignore
from dataclasses import dataclass, field
import re
from typing import Any, Generator, Literal


# usage: python ./scripts/linkchecker.py

print(
    '(Note: run "python ./scripts/docs.py build-all" before running this script and after switching branches)'
)


# Config


FASTAPI_REPO_ROOT = Path(__file__).parent.parent


# Types


MdPath = Path
HtmlPath = Path

DocumentId = str
HeadingId = str
LanguageId = str
Line = str
PatternSnippet = str

Level = int
LineNumber = int

IfInCode = bool


@dataclass
class Url:
    document: Document
    lnum: LineNumber
    type: str
    raw_url: str
    raw_path: str | None = None
    raw_hash: str | None = None
    translated_raw_hash: str | None = None
    target_document: Document | None = None
    target_en_document: Document | None = None
    target_type: Literal[
        "localhost", "pullrequest", "internal", "external"
    ] | None = None
    valid: bool | None = None


@dataclass
class Document:
    lang_id: LanguageId
    id: DocumentId
    md_path: MdPath
    html_path: HtmlPath
    virtualId: DocumentId | None = None
    heading_levels: list[Level] = field(default_factory=list)
    heading_ids: list[HeadingId] = field(default_factory=list)
    headings_in_sync_with_en_docs: bool | None = None
    urls: list[Url] = field(default_factory=list)
    same_number_of_urls_like_en_docs: bool | None = None


Documents = dict[LanguageId, dict[DocumentId, Document]]


# Patterns


html_headings_pattern = re.compile(
    r"""
    < \s* h([1-6]) \s+ id \s* = \s* " \s* ([^"\s]+) \s* "
    """,
    re.VERBOSE | re.IGNORECASE,
)

md_in_code_link_pattern = re.compile(
    r"""
    [{]! >? \s*
    ( \S+? )                                # 1
    (?: \[ ln: [0-9]+ - [0-9]+ \] )?
    \s* ![}]
    """,
    re.VERBOSE | re.IGNORECASE,
)

md_link_pattern = re.compile(
    r"""
    (?:
        <a (?:
            \s+ (?!href) [a-z]+ \s* = \s*
            (["'])                              # 1
            .*? \1
        )*
        \s+ href \s* = \s*
        (["'])                                  # 2
        \s* (?![{][{])
        (\S+?)                                  # 3
        \s* \2
    ) | (?:
        <img (?:
            \s+ (?!src) [a-z]+ \s* = \s*
            (["'])                              # 4
            .*? \4
        )*
        \s+ src \s* = \s*
        (["'])                                  # 5
        \s* (?![{][{])
        (\S+?)                                  # 6
        \s* \5
    ) | (?:
        (!)?                                    # 7
        \[ [^\]]+ \]
        \(
            ( [^)]+ )                           # 8
        \)
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)


# Functions


def exit_docs_not_compiled(message: str):
    print(
        f"ERROR: {message}. Please compile the documentation by running "
        '"python ./scripts/docs.py build-all"'
    )
    import sys

    sys.exit(1)


def iter_lines_and_context(
    filepath: Path,
) -> Generator[tuple[LineNumber, Line, IfInCode], Any, None]:
    with filepath.open("r", encoding="utf-8") as f:
        in_code = False
        for lnum, line in enumerate(f, start=1):
            line = line.lstrip()
            if line:
                if line.startswith("```"):
                    in_code = not in_code
                    continue
                yield (lnum, line, in_code)


def iter_documents(
    documents: Documents,
) -> Generator[Document, Any, None]:
    for lang_documents in documents.values():
        for document in lang_documents.values():
            yield document


def iter_urls(
    documents: Documents,
) -> Generator[Url, Any, None]:
    for document in iter_documents(documents):
        for url in document.urls:
            yield url


# Set up paths


markdown_root = FASTAPI_REPO_ROOT / "docs"
html_root = FASTAPI_REPO_ROOT / "site_build"
try:
    html_root = html_root.resolve(strict=True)
except FileNotFoundError:
    exit_docs_not_compiled(
        f'The directory "{html_root}", which is the compiled documentation, '
        "does not exist"
    )
resources_reference_point = markdown_root / "en/docs"


# Find all documents


print("checking internal links ...")

documents: Documents = {}

for lang_id in sorted(
    entry.name for entry in os.scandir(markdown_root) if entry.is_dir()
):
    unsorted: dict[DocumentId, Document] = {}
    md_lang_root = markdown_root / lang_id / "docs"
    md_lang_root_len = len(str(md_lang_root)) + 1
    html_lang_root = html_root / lang_id
    try:
        html_lang_root = html_lang_root.resolve(strict=True)
    except FileNotFoundError:
        exit_docs_not_compiled(
            f'The directory "{html_lang_root}", matching "{md_lang_root}", does not exist'
        )
    for root, _, files in os.walk(md_lang_root):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                document_id = md_path[md_lang_root_len:-3]
                if document_id.endswith("index"):
                    html_path = html_lang_root / (document_id + os.path.extsep + "html")
                else:
                    html_path = html_lang_root / (
                        os.path.join(document_id, "index.html")
                    )
                try:
                    html_path = html_path.resolve(strict=True)
                except FileNotFoundError:
                    exit_docs_not_compiled(
                        f'"{html_path}", the html document for "{md_path}" does not exist'
                    )
                unsorted[document_id] = Document(
                    id=document_id,
                    lang_id=lang_id,
                    md_path=Path(md_path),
                    html_path=html_path,
                )
    documents[lang_id] = dict(sorted(unsorted.items()))


# Find all headings and their IDs in the documents


for lang_id, lang_documents in documents.items():
    for document_id, document in lang_documents.items():
        text = document.html_path.read_text(encoding="utf-8")
        for match in html_headings_pattern.finditer(text):
            level, heading_id = match.groups()
            document.heading_levels.append(int(level))
            document.heading_ids.append(heading_id)


# Check if documents exist in the englisch docs and if the structure of their headings match


en_documents = documents["en"]

for lang_id, lang_documents in documents.items():
    if lang_id == "en":
        continue
    for document_id, document in lang_documents.items():
        if document_id not in en_documents:
            document.virtualId = str(Path(document.id).parent / "index")
        else:
            if document.heading_levels == en_documents[document_id].heading_levels:
                document.headings_in_sync_with_en_docs = True
            else:
                document.headings_in_sync_with_en_docs = False


# Parse all the urls in the documents


for document in iter_documents(documents):
    for lnum, line, in_code in iter_lines_and_context(document.md_path):
        if in_code:
            for match in md_in_code_link_pattern.finditer(line):
                document.urls.append(
                    Url(raw_url=match[1], type="code", document=document, lnum=lnum)
                )
        else:
            for match in md_link_pattern.finditer(line):
                if match[3]:
                    url = Url(
                        raw_url=match[3], type="link", document=document, lnum=lnum
                    )
                elif match[6]:
                    url = Url(
                        raw_url=match[6], type="image", document=document, lnum=lnum
                    )
                else:
                    url = Url(
                        raw_url=match[8],
                        type="image" if match[7] else "link",
                        document=document,
                        lnum=lnum,
                    )
                document.urls.append(url)


# Check if documents have the same amount of urls


for document in iter_documents(documents):
    if document.lang_id == "en" or document.virtualId:
        continue
    if len(document.urls) == len(en_documents[document.id].urls):
        document.same_number_of_urls_like_en_docs = True
    else:
        document.same_number_of_urls_like_en_docs = False


# Collect more infos about the urls


for url in iter_urls(documents):
    # Check the url target type (we only do stuff with internal urls so far)

    raw_url = url.raw_url
    if raw_url.startswith("http://") or raw_url.startswith("https://"):
        if (
            raw_url.startswith("http://127.")
            or raw_url.startswith("http://192.")
            or raw_url.startswith("http://localhost")
        ):
            url.target_type = "localhost"
            url.valid = True
        elif raw_url.startswith("https://github.com/tiangolo/fastapi/pull/"):
            url.target_type = "pullrequest"
            url.valid = True
        else:
            url.target_type = "external"
    else:
        url.target_type = "internal"

    # Check if internal code urls are valid

    if url.type == "code":
        try:
            (resources_reference_point / url.raw_url).resolve(strict=True)
        except FileNotFoundError:
            url.valid = False
        else:
            url.valid = True

    # Check if internal image urls are valid

    elif url.type == "image" and url.raw_url.startswith("/"):
        try:
            (resources_reference_point / url.raw_url[1:]).resolve(strict=True)
        except FileNotFoundError:
            url.valid = False
        else:
            url.valid = True

    # Check if internal links are valid

    elif url.type == "link" and url.target_type == "internal":
        # find the path part and hash part

        raw = url.raw_url.split("#")
        path = ""
        hash = ""
        len_raw = len(raw)
        if len_raw > 2:
            url.valid = False
        elif len_raw == 2:
            path, hash = raw
            if not hash:
                url.valid = False
        else:
            path = raw[0]

        url.raw_path = path
        url.raw_hash = hash

        # Now check

        if path:
            if (
                # './' is not necessary
                path.startswith("./")
                # Mkdocs complains about absolute urls
                or path.startswith("/")
                # Lets write `index.md` out, simpler to grasp.
                # E.g. "/#foo" can be confused with "#foo" but "index.md#foo" is explicit.
                # or, is "deployment/" "deployment.md" or "deployment/index.md"?
                or not path.endswith(".md")
            ):
                url.valid = False

        if url.valid is not False:
            url_document = url.document
            url_document_id = url_document.id

            # Check hash-only links

            if not path:
                if hash in url_document.heading_ids or (
                    url_document_id in en_documents
                    and hash in en_documents[url_document_id].heading_ids
                ):
                    url.valid = True
                else:
                    url.valid = False

            # Check links with a path part

            else:
                # Check if the path part is valid

                targetpath = None
                if url_document_id in en_documents:
                    targetpath = en_documents[url_document_id].md_path.parent / path
                else:
                    virtual_id = url.document.virtualId
                    if virtual_id is None:
                        raise Exception("make type checker happy")
                    else:
                        targetpath = en_documents[virtual_id].md_path.parent / path
                try:
                    targetpath = targetpath.resolve(strict=True)
                except FileNotFoundError:
                    try:
                        targetpath = (url_document.md_path.parent / path).resolve(
                            strict=True
                        )
                    except FileNotFoundError:
                        url.valid = False
                        targetpath = None

                # If the path part is valid and there is a hash part, check that too

                if targetpath:
                    if hash:
                        target_document_id = str(targetpath)[
                            len(str(resources_reference_point)) + 1 : -3
                        ]

                        if target_document_id in en_documents:
                            en_document = en_documents[target_document_id]
                        else:
                            en_document = None

                        lang_id = url.document.lang_id
                        if target_document_id in documents[lang_id]:
                            lang_document = documents[lang_id][target_document_id]
                        else:
                            lang_document = None

                        url.target_document = lang_document
                        url.target_en_document = en_document

                        if en_document and hash in en_document.heading_ids:
                            url.valid = True
                            if (
                                lang_document
                                # and url.document.same_number_of_urls_like_en_docs
                                and lang_document.headings_in_sync_with_en_docs
                            ):
                                lang_hash = lang_document.heading_ids[
                                    en_document.heading_ids.index(hash)
                                ]
                                if hash != lang_hash:
                                    url.translated_raw_hash = lang_hash
                        elif lang_document and hash in lang_document.heading_ids:
                            url.valid = True
                        else:
                            url.valid = False

                    # If there is no hash, the url is valid as already checked.

                    else:
                        url.valid = True


# Print invalid urls


invalid_urls: list[Url] = []

for url in iter_urls(documents):
    if url.valid == False:
        invalid_urls.append(url)

if invalid_urls:
    print("    Invalid urls:")
    for url in invalid_urls:
        print(f"        {url.document.lang_id} | {url.document.id} | {url.raw_url}")
    print(
        "    Note: Invalid hashes in DE urls will resolve, when the target document PR is merged. In my all-in-one branch they resolve."
    )
else:
    print("    All urls are valid")


# Print possibly translatable hashes


translatable_hashes: dict[str, list[str]] = {}

for url in iter_urls(documents):
    if url.translated_raw_hash:
        id = f"{url.document.lang_id}/{url.document.id}"
        if id not in translatable_hashes:
            translatable_hashes[id] = []
        translatable_hashes[id].append(
            f"        {url.raw_url} -> {url.raw_path}#{url.translated_raw_hash}"
        )

if translatable_hashes:
    print("The hashes of these urls may possibly be translated. Please check manually:")
    for id in translatable_hashes:
        print(f"    {id}.md")
        for comparision in translatable_hashes[id]:
            print(comparision)


# TBD maybe: check external links


# externals: set[str] = set()

# for url in iter_urls(documents):
#     if url.target == "external":
#         externals.add(url.raw)
#         # if not url.external and url.valid != True:
#         # print(url.document.lang_id, url.document.id, url.raw)

# for url in externals:
#     with httpx.Client() as client:
#         r = client.head(url)
#         # print("OK" if r.is_success else "ERROR", r.url)
#         print(r.status_code, r.url)


# End
