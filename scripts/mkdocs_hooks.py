from typing import Any, List, Union

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Link, Navigation, Section
from mkdocs.structure.pages import Page


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
