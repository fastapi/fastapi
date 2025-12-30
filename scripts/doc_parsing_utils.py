import re
from typing import TypedDict

CODE_INCLUDE_RE = re.compile(r"^\{\*\s*(\S+)\s*(.*)\*\}$")
CODE_INCLUDE_PLACEHOLDER = "<CODE_INCLUDE>"

HEADER_WITH_PERMALINK_RE = re.compile(r"^(#{1,6}) (.+?)(\s*\{\s*#.*\s*\})?\s*$")
HEADER_LINE_RE = re.compile(r"^(#{1,6}) (.+?)(?:\s*\{\s*(#.*)\s*\})?\s*$")

TIANGOLO_COM = "https://fastapi.tiangolo.com"

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
HTML_LINK_TEXT = re.compile(r"<a\b([^>]*)>(.*?)</a>")
HTML_LINK_OPEN_TAG_RE = re.compile(r"<a\b([^>]*)>")
HTML_ATTR_RE = re.compile(r'(\w+)\s*=\s*([\'"])(.*?)\2')


class CodeIncludeInfo(TypedDict):
    line_no: int
    line: str


class HeaderPermalinkInfo(TypedDict):
    line_no: int
    hashes: str
    permalink: str


class MarkdownLinkInfo(TypedDict):
    line_no: int
    url: str
    text: str
    title: str | None
    attributes: str | None


class HTMLLinkAttribute(TypedDict):
    name: str
    quote: str
    value: str


class HtmlLinkInfo(TypedDict):
    line_no: int
    full_tag: str
    attributes: list[HTMLLinkAttribute]
    text: str


# Code includes
# -----------------------------------------------------------------------------------------


def extract_code_includes(lines: list[str]) -> list[CodeIncludeInfo]:
    """
    Exctract lines that contain code includes.

    Return list of CodeIncludeInfo namedtuples, where each tuple contains:
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

    includes = extract_code_includes(text)
    for include in includes:
        text[include["line_no"] - 1] = CODE_INCLUDE_PLACEHOLDER
    return text


def replace_placeholders_with_code_includes(
    text: list[str], original_includes: list[CodeIncludeInfo]
) -> list[str]:
    """
    Replace code includes placeholders with actual code includes from the original (English) document.
    Fail if the number of placeholders does not match the number of original includes.
    """

    modified_text: list[str] = []
    include_index = 0
    for line in text:
        if line.strip() == CODE_INCLUDE_PLACEHOLDER:
            if include_index >= len(original_includes):
                raise ValueError(
                    "Number of placeholders exceeds number of code includes in the original document"
                )
            modified_text.append(original_includes[include_index]["line"])
            include_index += 1
        else:
            modified_text.append(line)

    if include_index < len(original_includes):
        raise ValueError(
            "Number of placeholders is less than number of code includes in the original document"
        )

    return modified_text


# Header permalinks
# -----------------------------------------------------------------------------------------


def extract_header_permalinks(lines: list[str]) -> list[HeaderPermalinkInfo]:
    """
    Extract list of header permalinks from the given lines.

    Return list of HeaderPermalinkInfo namedtuples, where each tuple contains:
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
                hashes, _title, permalink = header_match.groups()
                headers.append(
                    HeaderPermalinkInfo(
                        hashes=hashes, line_no=line_no, permalink=permalink
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
    text: list[str], original_permalinks: list[HeaderPermalinkInfo]
) -> list[str]:
    """
    Replace permalinks in the given text with the permalinks from the original document.

    Fail if the number or order of headers does not match the original.
    """

    modified_text: list[str] = []
    permalink_index = 0
    for line in text:
        header_match = HEADER_LINE_RE.match(line)
        if header_match:
            if permalink_index >= len(original_permalinks):
                raise ValueError(
                    "Number of headers exceeds number of headers in the original document"
                )
            hashes, title, _permalink = header_match.groups()
            original_permalink_info = original_permalinks[permalink_index]
            if original_permalink_info["hashes"] != hashes:
                raise ValueError(
                    "Header levels do not match between document and original document"
                )

            modified_line = f"{hashes} {title}{original_permalink_info['permalink']}"
            modified_text.append(modified_line)
            permalink_index += 1
        else:
            modified_text.append(line)

    if permalink_index < len(original_permalinks):
        raise ValueError(
            "Number of headers is less than number of headers in the original document"
        )

    return modified_text


# Markdown links
# -----------------------------------------------------------------------------------------


def extract_markdown_links(lines: list[str]) -> list[tuple[str, int]]:
    """
    Extract all markdown links from the given lines.

    Return list of MarkdownLinkInfo namedtuples, where each tuple contains:
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
                )
            )
    return links


def _construct_markdown_link(
    url: str, text: str, title: str | None, attributes: str | None, lang_code: str
) -> str:
    """
    Construct a markdown link, adjusting the URL for the given language code if needed.
    """

    if url.startswith(TIANGOLO_COM):
        url = url.replace(TIANGOLO_COM, f"{TIANGOLO_COM}/{lang_code}")

    if title:
        link = f'[{text}]({url} "{title}")'
    else:
        link = f"[{text}]({url})"

    if attributes:
        link += f" {{{attributes}}}"

    return link


def replace_markdown_links(
    text: list[str], original_links: list[MarkdownLinkInfo], lang_code: str
) -> list[str]:
    """
    Replace markdown links in the given text with the original links.

    Fail if the number of links does not match the original.
    """

    modified_text: list[str] = []
    link_index = 0
    for line in text:
        modified_line = line
        for m in MARKDOWN_LINK_RE.finditer(line):
            if link_index >= len(original_links):
                raise ValueError(
                    "Number of markdown links exceeds number of markdown links in the original document"
                )
            link_text = m.group("text")
            assert isinstance(link_text, str)
            link_title = m.group("title")
            assert link_title is None or isinstance(link_title, str)

            original_link_info = original_links[link_index]

            # Replace
            replacement_link = _construct_markdown_link(
                url=original_link_info["url"],
                text=link_text,
                title=link_title,
                attributes=original_link_info["attributes"],
                lang_code=lang_code,
            )
            modified_line = modified_line.replace(m.group(0), replacement_link, 1)

            link_index += 1
        modified_text.append(modified_line)

    if link_index < len(original_links):
        raise ValueError(
            "Number of markdown links is less than in the original document"
        )

    return modified_text


# HTML links
# -----------------------------------------------------------------------------------------


def extract_html_links(lines: list[str]) -> list[HtmlLinkInfo]:
    """
    Extract all HTML links from the given lines.

    Return list of HtmlLinkInfo namedtuples, where each tuple contains:
    - `line_no` - line number (1-based)
    - `full_tag` - full HTML link tag
    - `attributes` - list of HTMLLinkAttribute namedtuples (name, quote, value)
    - `text` - link text
    """

    links = []
    for line_no, line in enumerate(lines, start=1):
        for html_link in HTML_LINK_RE.finditer(line):
            link_str = html_link.group(0)

            link_text_match = HTML_LINK_TEXT.match(link_str)
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
            if original_url.startswith(TIANGOLO_COM):
                url = original_url.replace(TIANGOLO_COM, f"{TIANGOLO_COM}/{lang_code}")
            else:
                url = original_url
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
    text: list[str], original_links: list[HtmlLinkInfo], lang_code: str
) -> list[str]:
    """
    Replace HTML links in the given text with the links from the original document.

    Adjust URLs for the given language code.
    Fail if the number of links does not match the original.
    """

    links = extract_html_links(text)
    if len(links) > len(original_links):
        raise ValueError(
            "Number of HTML links exceeds number of HTML links in the original document"
        )
    elif len(links) < len(original_links):
        raise ValueError("Number of HTML links is less than in the original document")

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
