from pathlib import Path
from typing import Any, List, Union

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Link, Navigation, Section
from mkdocs.structure.pages import Page

missing_translation_content = """
!!! warning
    The current page still doesn't have a translation for this language.

    But you can help translating it: [Contributing](https://fastapi.tiangolo.com/contributing/){.internal-link target=_blank}.
"""


class EnFile(File):
    pass


def on_config(config: MkDocsConfig, **kwargs) -> MkDocsConfig:
    dir_path = Path(config.docs_dir)
    lang = dir_path.parent.name
    config.theme["language"] = lang
    if not (config.site_url or "").endswith(f"{lang}/") and not lang == "en":
        config.site_url = f"{config.site_url}{lang}/"
    return config


def resolve_file(*, item: str, files: Files, config: MkDocsConfig) -> None:
    item_path = Path(config.docs_dir) / item
    if not item_path.is_file():
        en_src_dir = (Path(config.docs_dir) / "../../en/docs").resolve()
        potential_path = en_src_dir / item
        if potential_path.is_file():
            files.append(
                EnFile(
                    path=item,
                    src_dir=str(en_src_dir),
                    dest_dir=config.site_dir,
                    use_directory_urls=config.use_directory_urls,
                )
            )


def resolve_files(*, items: List[Any], files: Files, config: MkDocsConfig) -> None:
    for item in items:
        if isinstance(item, str):
            resolve_file(item=item, files=files, config=config)
        elif isinstance(item, dict):
            assert len(item) == 1
            values = list(item.values())
            if not values:
                continue
            if isinstance(values[0], str):
                resolve_file(item=values[0], files=files, config=config)
            elif isinstance(values[0], list):
                resolve_files(items=values[0], files=files, config=config)
            else:
                raise ValueError(f"Unexpected value: {values}")


def on_files(files: Files, *, config: MkDocsConfig) -> Files:
    resolve_files(items=config.nav or [], files=files, config=config)
    if "logo" in config.theme:
        resolve_file(item=config.theme["logo"], files=files, config=config)
    if "favicon" in config.theme:
        resolve_file(item=config.theme["favicon"], files=files, config=config)
    resolve_files(items=config.extra_css, files=files, config=config)
    resolve_files(items=config.extra_javascript, files=files, config=config)
    return files


def generate_renamed_section_items(
    items: List[Union[Page, Section, Link]], *, config: MkDocsConfig
) -> List[Union[Page, Section, Link]]:
    new_items: List[Union[Page, Section, Link]] = []
    for item in items:
        if isinstance(item, Section):
            new_title = item.title
            new_children = generate_renamed_section_items(item.children, config=config)
            first_child = new_children[0]
            if isinstance(first_child, Page):
                if first_child.file.src_path.endswith("index.md"):
                    # Read the source so that the title is parsed and available
                    first_child.read_source(config=config)
                    new_title = first_child.title or new_title
            # Creating a new section makes it render it collapsed by default
            # no idea why, so, let's just modify the existing one
            # new_section = Section(title=new_title, children=new_children)
            item.title = new_title
            item.children = new_children
            new_items.append(item)
        else:
            new_items.append(item)
    return new_items


def on_nav(
    nav: Navigation, *, config: MkDocsConfig, files: Files, **kwargs: Any
) -> Navigation:
    new_items = generate_renamed_section_items(nav.items, config=config)
    return Navigation(items=new_items, pages=nav.pages)


def on_pre_page(page: Page, *, config: MkDocsConfig, files: Files) -> Page:
    return page


def on_page_markdown(
    markdown: str, *, page: Page, config: MkDocsConfig, files: Files
) -> str:
    if isinstance(page.file, EnFile):
        header = ""
        body = markdown
        if markdown.startswith("#"):
            header, _, body = markdown.partition("\n\n")
        return f"{header}\n\n{missing_translation_content}\n\n{body}"
    return markdown
