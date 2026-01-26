import re
from typing import TypedDict, Union

CODE_INCLUDE_RE = re.compile(r"^\{\*\s*(\S+)\s*(.*)\*\}$")
CODE_INCLUDE_PLACEHOLDER = "<CODE_INCLUDE>"

HEADER_WITH_PERMALINK_RE = re.compile(r"^(#{1,6}) (.+?)(\s*\{\s*#.*\s*\})?\s*$")
HEADER_LINE_RE = re.compile(r"^(#{1,6}) (.+?)(?:\s*\{\s*(#.*)\s*\})?\s*$")

TIANGOLO_COM = "https://fastapi.tiangolo.com"
ASSETS_URL_PREFIXES = ("/img/", "/css/", "/js/")

MARKDOWN_LINK_RE = re.compile(
    r"(?<!\\)(?<!\!)"  # not an image ![...] and not escaped \[...]
    r"\[(?P<text>.*?)\]"  # link text (non-greedy)
    r"\("
    r"(?P<url>[^)\s]+)"  # url (no spaces and `)`)
    r'(?:\s+["\'](?P<title>.*?)["\'])?'  # optional title in "" or ''
    r"\)"
    r"(?:\s*\{(?P<attrs>[^}]*)\})?"  # optional attributes in {}
)

HTML_LINK_RE = re.compile(r"<a\s+[^>]*>.*?</a>")
HTML_LINK_TEXT_RE = re.compile(r"<a\b([^>]*)>(.*?)</a>")
HTML_LINK_OPEN_TAG_RE = re.compile(r"<a\b([^>]*)>")
HTML_ATTR_RE = re.compile(r'(\w+)\s*=\s*([\'"])(.*?)\2')

CODE_BLOCK_LANG_RE = re.compile(r"^`{3,4}([\w-]*)", re.MULTILINE)

SLASHES_COMMENT_RE = re.compile(
    r"^(?P<code>.*?)(?P<comment>(?:(?<= )// .*)|(?:^// .*))?$"
)

HASH_COMMENT_RE = re.compile(r"^(?P<code>.*?)(?P<comment>(?:(?<= )# .*)|(?:^# .*))?$")


class CodeIncludeInfo(TypedDict):
    line_no: int
    line: str


class HeaderPermalinkInfo(TypedDict):
    line_no: int
    hashes: str
    title: str
    permalink: str


class MarkdownLinkInfo(TypedDict):
    line_no: int
    url: str
    text: str
    title: Union[str, None]
    attributes: Union[str, None]
    full_match: str


class HTMLLinkAttribute(TypedDict):
    name: str
    quote: str
    value: str


class HtmlLinkInfo(TypedDict):
    line_no: int
    full_tag: str
    attributes: list[HTMLLinkAttribute]
    text: str


class MultilineCodeBlockInfo(TypedDict):
    lang: str
    start_line_no: int
    content: list[str]


# Code includes
# --------------------------------------------------------------------------------------


def extract_code_includes(lines: list[str]) -> list[CodeIncludeInfo]:
    """
    Extract lines that contain code includes.

    Return list of CodeIncludeInfo, where each dict contains:
    - `line_no` - line number (1-based)
    - `line` - text of the line
    """

    includes: list[CodeIncludeInfo] = []
    for line_no, line in enumerate(lines, start=1):
        if CODE_INCLUDE_RE.match(line):
            includes.append(CodeIncludeInfo(line_no=line_no, line=line))
    return includes


def replace_code_includes_with_placeholders(text: list[str]) -> list[str]:
    """
    Replace code includes with placeholders.
    """

    modified_text = text.copy()
    includes = extract_code_includes(text)
    for include in includes:
        modified_text[include["line_no"] - 1] = CODE_INCLUDE_PLACEHOLDER
    return modified_text


def replace_placeholders_with_code_includes(
    text: list[str], original_includes: list[CodeIncludeInfo]
) -> list[str]:
    """
    Replace code includes placeholders with actual code includes from the original (English) document.
    Fail if the number of placeholders does not match the number of original includes.
    """

    code_include_lines = [
        line_no
        for line_no, line in enumerate(text)
        if line.strip() == CODE_INCLUDE_PLACEHOLDER
    ]

    if len(code_include_lines) != len(original_includes):
        raise ValueError(
            "Number of code include placeholders does not match the number of code includes "
            "in the original document "
            f"({len(code_include_lines)} vs {len(original_includes)})"
        )

    modified_text = text.copy()
    for i, line_no in enumerate(code_include_lines):
        modified_text[line_no] = original_includes[i]["line"]

    return modified_text


# Header permalinks
# --------------------------------------------------------------------------------------


def extract_header_permalinks(lines: list[str]) -> list[HeaderPermalinkInfo]:
    """
    Extract list of header permalinks from the given lines.

    Return list of HeaderPermalinkInfo, where each dict contains:
    - `line_no` - line number (1-based)
    - `hashes` - string of hashes representing header level (e.g., "###")
    - `permalink` - permalink string (e.g., "{#permalink}")
    """

    headers: list[HeaderPermalinkInfo] = []
    in_code_block3 = False
    in_code_block4 = False

    for line_no, line in enumerate(lines, start=1):
        if not (in_code_block3 or in_code_block4):
            if line.startswith("```"):
                count = len(line) - len(line.lstrip("`"))
                if count == 3:
                    in_code_block3 = True
                    continue
                elif count >= 4:
                    in_code_block4 = True
                    continue

            header_match = HEADER_WITH_PERMALINK_RE.match(line)
            if header_match:
                hashes, title, permalink = header_match.groups()
                headers.append(
                    HeaderPermalinkInfo(
                        hashes=hashes, line_no=line_no, permalink=permalink, title=title
                    )
                )

        elif in_code_block3:
            if line.startswith("```"):
                count = len(line) - len(line.lstrip("`"))
                if count == 3:
                    in_code_block3 = False
                    continue

        elif in_code_block4:
            if line.startswith("````"):
                count = len(line) - len(line.lstrip("`"))
                if count >= 4:
                    in_code_block4 = False
                    continue

    return headers


def remove_header_permalinks(lines: list[str]) -> list[str]:
    """
    Remove permalinks from headers in the given lines.
    """

    modified_lines: list[str] = []
    for line in lines:
        header_match = HEADER_WITH_PERMALINK_RE.match(line)
        if header_match:
            hashes, title, _permalink = header_match.groups()
            modified_line = f"{hashes} {title}"
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)
    return modified_lines


def replace_header_permalinks(
    text: list[str],
    header_permalinks: list[HeaderPermalinkInfo],
    original_header_permalinks: list[HeaderPermalinkInfo],
) -> list[str]:
    """
    Replace permalinks in the given text with the permalinks from the original document.

    Fail if the number or level of headers does not match the original.
    """

    modified_text: list[str] = text.copy()

    if len(header_permalinks) != len(original_header_permalinks):
        raise ValueError(
            "Number of headers with permalinks does not match the number in the "
            "original document "
            f"({len(header_permalinks)} vs {len(original_header_permalinks)})"
        )

    for header_no in range(len(header_permalinks)):
        header_info = header_permalinks[header_no]
        original_header_info = original_header_permalinks[header_no]

        if header_info["hashes"] != original_header_info["hashes"]:
            raise ValueError(
                "Header levels do not match between document and original document"
                f" (found {header_info['hashes']}, expected {original_header_info['hashes']})"
                f" for header №{header_no + 1} in line {header_info['line_no']}"
            )
        line_no = header_info["line_no"] - 1
        hashes = header_info["hashes"]
        title = header_info["title"]
        permalink = original_header_info["permalink"]
        modified_text[line_no] = f"{hashes} {title}{permalink}"

    return modified_text


# Markdown links
# --------------------------------------------------------------------------------------


def extract_markdown_links(lines: list[str]) -> list[MarkdownLinkInfo]:
    """
    Extract all markdown links from the given lines.

    Return list of MarkdownLinkInfo, where each dict contains:
    - `line_no` - line number (1-based)
    - `url` - link URL
    - `text` - link text
    - `title` - link title (if any)
    """

    links: list[MarkdownLinkInfo] = []
    for line_no, line in enumerate(lines, start=1):
        for m in MARKDOWN_LINK_RE.finditer(line):
            links.append(
                MarkdownLinkInfo(
                    line_no=line_no,
                    url=m.group("url"),
                    text=m.group("text"),
                    title=m.group("title"),
                    attributes=m.group("attrs"),
                    full_match=m.group(0),
                )
            )
    return links


def _add_lang_code_to_url(url: str, lang_code: str) -> str:
    if url.startswith(TIANGOLO_COM):
        rel_url = url[len(TIANGOLO_COM) :]
        if not rel_url.startswith(ASSETS_URL_PREFIXES):
            url = url.replace(TIANGOLO_COM, f"{TIANGOLO_COM}/{lang_code}")
    return url


def _construct_markdown_link(
    url: str,
    text: str,
    title: Union[str, None],
    attributes: Union[str, None],
    lang_code: str,
) -> str:
    """
    Construct a markdown link, adjusting the URL for the given language code if needed.
    """
    url = _add_lang_code_to_url(url, lang_code)

    if title:
        link = f'[{text}]({url} "{title}")'
    else:
        link = f"[{text}]({url})"

    if attributes:
        link += f"{{{attributes}}}"

    return link


def replace_markdown_links(
    text: list[str],
    links: list[MarkdownLinkInfo],
    original_links: list[MarkdownLinkInfo],
    lang_code: str,
) -> list[str]:
    """
    Replace markdown links in the given text with the original links.

    Fail if the number of links does not match the original.
    """

    if len(links) != len(original_links):
        raise ValueError(
            "Number of markdown links does not match the number in the "
            "original document "
            f"({len(links)} vs {len(original_links)})"
        )

    modified_text = text.copy()
    for i, link_info in enumerate(links):
        link_text = link_info["text"]
        link_title = link_info["title"]
        original_link_info = original_links[i]

        # Replace
        replacement_link = _construct_markdown_link(
            url=original_link_info["url"],
            text=link_text,
            title=link_title,
            attributes=original_link_info["attributes"],
            lang_code=lang_code,
        )
        line_no = link_info["line_no"] - 1
        modified_line = modified_text[line_no]
        modified_line = modified_line.replace(
            link_info["full_match"], replacement_link, 1
        )
        modified_text[line_no] = modified_line

    return modified_text


# HTML links
# --------------------------------------------------------------------------------------


def extract_html_links(lines: list[str]) -> list[HtmlLinkInfo]:
    """
    Extract all HTML links from the given lines.

    Return list of HtmlLinkInfo, where each dict contains:
    - `line_no` - line number (1-based)
    - `full_tag` - full HTML link tag
    - `attributes` - list of HTMLLinkAttribute (name, quote, value)
    - `text` - link text
    """

    links = []
    for line_no, line in enumerate(lines, start=1):
        for html_link in HTML_LINK_RE.finditer(line):
            link_str = html_link.group(0)

            link_text_match = HTML_LINK_TEXT_RE.match(link_str)
            assert link_text_match is not None
            link_text = link_text_match.group(2)
            assert isinstance(link_text, str)

            link_open_tag_match = HTML_LINK_OPEN_TAG_RE.match(link_str)
            assert link_open_tag_match is not None
            link_open_tag = link_open_tag_match.group(1)
            assert isinstance(link_open_tag, str)

            attributes: list[HTMLLinkAttribute] = []
            for attr_name, attr_quote, attr_value in re.findall(
                HTML_ATTR_RE, link_open_tag
            ):
                assert isinstance(attr_name, str)
                assert isinstance(attr_quote, str)
                assert isinstance(attr_value, str)
                attributes.append(
                    HTMLLinkAttribute(
                        name=attr_name, quote=attr_quote, value=attr_value
                    )
                )
            links.append(
                HtmlLinkInfo(
                    line_no=line_no,
                    full_tag=link_str,
                    attributes=attributes,
                    text=link_text,
                )
            )
    return links


def _construct_html_link(
    link_text: str,
    attributes: list[HTMLLinkAttribute],
    lang_code: str,
) -> str:
    """
    Reconstruct HTML link, adjusting the URL for the given language code if needed.
    """

    attributes_upd: list[HTMLLinkAttribute] = []
    for attribute in attributes:
        if attribute["name"] == "href":
            original_url = attribute["value"]
            url = _add_lang_code_to_url(original_url, lang_code)
            attributes_upd.append(
                HTMLLinkAttribute(name="href", quote=attribute["quote"], value=url)
            )
        else:
            attributes_upd.append(attribute)

    attrs_str = " ".join(
        f"{attribute['name']}={attribute['quote']}{attribute['value']}{attribute['quote']}"
        for attribute in attributes_upd
    )
    return f"<a {attrs_str}>{link_text}</a>"


def replace_html_links(
    text: list[str],
    links: list[HtmlLinkInfo],
    original_links: list[HtmlLinkInfo],
    lang_code: str,
) -> list[str]:
    """
    Replace HTML links in the given text with the links from the original document.

    Adjust URLs for the given language code.
    Fail if the number of links does not match the original.
    """

    if len(links) != len(original_links):
        raise ValueError(
            "Number of HTML links does not match the number in the "
            "original document "
            f"({len(links)} vs {len(original_links)})"
        )

    modified_text = text.copy()
    for link_index, link in enumerate(links):
        original_link_info = original_links[link_index]

        # Replace in the document text
        replacement_link = _construct_html_link(
            link_text=link["text"],
            attributes=original_link_info["attributes"],
            lang_code=lang_code,
        )
        line_no = link["line_no"] - 1
        modified_text[line_no] = modified_text[line_no].replace(
            link["full_tag"], replacement_link, 1
        )

    return modified_text


# Multiline code blocks
# --------------------------------------------------------------------------------------


def get_code_block_lang(line: str) -> str:
    match = CODE_BLOCK_LANG_RE.match(line)
    if match:
        return match.group(1)
    return ""


def extract_multiline_code_blocks(text: list[str]) -> list[MultilineCodeBlockInfo]:
    blocks: list[MultilineCodeBlockInfo] = []

    in_code_block3 = False
    in_code_block4 = False
    current_block_lang = ""
    current_block_start_line = -1
    current_block_lines = []

    for line_no, line in enumerate(text, start=1):
        stripped = line.lstrip()

        # --- Detect opening fence ---
        if not (in_code_block3 or in_code_block4):
            if stripped.startswith("```"):
                current_block_start_line = line_no
                count = len(stripped) - len(stripped.lstrip("`"))
                if count == 3:
                    in_code_block3 = True
                    current_block_lang = get_code_block_lang(stripped)
                    current_block_lines = [line]
                    continue
                elif count >= 4:
                    in_code_block4 = True
                    current_block_lang = get_code_block_lang(stripped)
                    current_block_lines = [line]
                    continue

        # --- Detect closing fence ---
        elif in_code_block3:
            if stripped.startswith("```"):
                count = len(stripped) - len(stripped.lstrip("`"))
                if count == 3:
                    current_block_lines.append(line)
                    blocks.append(
                        MultilineCodeBlockInfo(
                            lang=current_block_lang,
                            start_line_no=current_block_start_line,
                            content=current_block_lines,
                        )
                    )
                    in_code_block3 = False
                    current_block_lang = ""
                    current_block_start_line = -1
                    current_block_lines = []
                    continue
            current_block_lines.append(line)

        elif in_code_block4:
            if stripped.startswith("````"):
                count = len(stripped) - len(stripped.lstrip("`"))
                if count >= 4:
                    current_block_lines.append(line)
                    blocks.append(
                        MultilineCodeBlockInfo(
                            lang=current_block_lang,
                            start_line_no=current_block_start_line,
                            content=current_block_lines,
                        )
                    )
                    in_code_block4 = False
                    current_block_lang = ""
                    current_block_start_line = -1
                    current_block_lines = []
                    continue
            current_block_lines.append(line)

    return blocks


def _split_hash_comment(line: str) -> tuple[str, Union[str, None]]:
    match = HASH_COMMENT_RE.match(line)
    if match:
        code = match.group("code").rstrip()
        comment = match.group("comment")
        return code, comment
    return line.rstrip(), None


def _split_slashes_comment(line: str) -> tuple[str, Union[str, None]]:
    match = SLASHES_COMMENT_RE.match(line)
    if match:
        code = match.group("code").rstrip()
        comment = match.group("comment")
        return code, comment
    return line, None


def replace_multiline_code_block(
    block_a: MultilineCodeBlockInfo, block_b: MultilineCodeBlockInfo
) -> list[str]:
    """
    Replace multiline code block `a` with block `b` leaving comments intact.

    Syntax of comments depends on the language of the code block.
    Raises ValueError if the blocks are not compatible (different languages or different number of lines).
    """

    start_line = block_a["start_line_no"]
    end_line_no = start_line + len(block_a["content"]) - 1

    if block_a["lang"] != block_b["lang"]:
        raise ValueError(
            f"Code block (lines {start_line}-{end_line_no}) "
            "has different language than the original block "
            f"('{block_a['lang']}' vs '{block_b['lang']}')"
        )
    if len(block_a["content"]) != len(block_b["content"]):
        raise ValueError(
            f"Code block (lines {start_line}-{end_line_no}) "
            "has different number of lines than the original block "
            f"({len(block_a['content'])} vs {len(block_b['content'])})"
        )

    block_language = block_a["lang"].lower()
    if block_language in {"mermaid"}:
        if block_a != block_b:
            print(
                f"Skipping mermaid code block replacement (lines {start_line}-{end_line_no}). "
                "This should be checked manually."
            )
        return block_a["content"].copy()  # We don't handle mermaid code blocks for now

    code_block: list[str] = []
    for line_a, line_b in zip(block_a["content"], block_b["content"]):
        line_a_comment: Union[str, None] = None
        line_b_comment: Union[str, None] = None

        # Handle comments based on language
        if block_language in {
            "python",
            "py",
            "sh",
            "bash",
            "dockerfile",
            "requirements",
            "gitignore",
            "toml",
            "yaml",
            "yml",
            "hash-style-comments",
        }:
            _line_a_code, line_a_comment = _split_hash_comment(line_a)
            _line_b_code, line_b_comment = _split_hash_comment(line_b)
            res_line = line_b
            if line_b_comment:
                res_line = res_line.replace(line_b_comment, line_a_comment, 1)
            code_block.append(res_line)
        elif block_language in {"console", "json", "slash-style-comments"}:
            _line_a_code, line_a_comment = _split_slashes_comment(line_a)
            _line_b_code, line_b_comment = _split_slashes_comment(line_b)
            res_line = line_b
            if line_b_comment:
                res_line = res_line.replace(line_b_comment, line_a_comment, 1)
            code_block.append(res_line)
        else:
            code_block.append(line_b)

    return code_block


def replace_multiline_code_blocks_in_text(
    text: list[str],
    code_blocks: list[MultilineCodeBlockInfo],
    original_code_blocks: list[MultilineCodeBlockInfo],
) -> list[str]:
    """
    Update each code block in `text` with the corresponding code block from
    `original_code_blocks` with comments taken from `code_blocks`.

    Raises ValueError if the number, language, or shape of code blocks do not match.
    """

    if len(code_blocks) != len(original_code_blocks):
        raise ValueError(
            "Number of code blocks does not match the number in the original document "
            f"({len(code_blocks)} vs {len(original_code_blocks)})"
        )

    modified_text = text.copy()
    for block, original_block in zip(code_blocks, original_code_blocks):
        updated_content = replace_multiline_code_block(block, original_block)

        start_line_index = block["start_line_no"] - 1
        for i, updated_line in enumerate(updated_content):
            modified_text[start_line_index + i] = updated_line

    return modified_text


# All checks
# --------------------------------------------------------------------------------------


def check_translation(
    doc_lines: list[str],
    en_doc_lines: list[str],
    lang_code: str,
    auto_fix: bool,
    path: str,
) -> list[str]:
    # Fix code includes
    en_code_includes = extract_code_includes(en_doc_lines)
    doc_lines_with_placeholders = replace_code_includes_with_placeholders(doc_lines)
    fixed_doc_lines = replace_placeholders_with_code_includes(
        doc_lines_with_placeholders, en_code_includes
    )
    if auto_fix and (fixed_doc_lines != doc_lines):
        print(f"Fixing code includes in: {path}")
        doc_lines = fixed_doc_lines

    # Fix permalinks
    en_permalinks = extract_header_permalinks(en_doc_lines)
    doc_permalinks = extract_header_permalinks(doc_lines)
    fixed_doc_lines = replace_header_permalinks(
        doc_lines, doc_permalinks, en_permalinks
    )
    if auto_fix and (fixed_doc_lines != doc_lines):
        print(f"Fixing header permalinks in: {path}")
        doc_lines = fixed_doc_lines

    # Fix markdown links
    en_markdown_links = extract_markdown_links(en_doc_lines)
    doc_markdown_links = extract_markdown_links(doc_lines)
    fixed_doc_lines = replace_markdown_links(
        doc_lines, doc_markdown_links, en_markdown_links, lang_code
    )
    if auto_fix and (fixed_doc_lines != doc_lines):
        print(f"Fixing markdown links in: {path}")
        doc_lines = fixed_doc_lines

    # Fix HTML links
    en_html_links = extract_html_links(en_doc_lines)
    doc_html_links = extract_html_links(doc_lines)
    fixed_doc_lines = replace_html_links(
        doc_lines, doc_html_links, en_html_links, lang_code
    )
    if auto_fix and (fixed_doc_lines != doc_lines):
        print(f"Fixing HTML links in: {path}")
        doc_lines = fixed_doc_lines

    # Fix multiline code blocks
    en_code_blocks = extract_multiline_code_blocks(en_doc_lines)
    doc_code_blocks = extract_multiline_code_blocks(doc_lines)
    fixed_doc_lines = replace_multiline_code_blocks_in_text(
        doc_lines, doc_code_blocks, en_code_blocks
    )
    if auto_fix and (fixed_doc_lines != doc_lines):
        print(f"Fixing multiline code blocks in: {path}")
        doc_lines = fixed_doc_lines

    return doc_lines
