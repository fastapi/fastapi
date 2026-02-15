import json
import logging
import os
import re
import shutil
import subprocess
from html.parser import HTMLParser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Pool
from pathlib import Path
from typing import Any

import mkdocs.utils
import typer
import yaml
from jinja2 import Template
from ruff.__main__ import find_ruff_bin
from slugify import slugify as py_slugify

logging.basicConfig(level=logging.INFO)

SUPPORTED_LANGS = {
    "de",
    "en",
    "es",
    "fr",
    "ja",
    "ko",
    "pt",
    "ru",
    "tr",
    "uk",
    "zh",
    "zh-hant",
}


app = typer.Typer()

mkdocs_name = "mkdocs.yml"

missing_translation_snippet = """
{!../../docs/missing-translation.md!}
"""

non_translated_sections = (
    f"reference{os.sep}",
    "release-notes.md",
    "fastapi-people.md",
    "external-links.md",
    "newsletter.md",
    "management-tasks.md",
    "management.md",
    "contributing.md",
)

docs_path = Path("docs")
en_docs_path = Path("docs/en")
en_config_path: Path = en_docs_path / mkdocs_name
site_path = Path("site").absolute()
build_site_path = Path("site_build").absolute()

header_pattern = re.compile(r"^(#{1,6}) (.+?)(?:\s*\{\s*(#.*)\s*\})?\s*$")
header_with_permalink_pattern = re.compile(r"^(#{1,6}) (.+?)(\s*\{\s*#.*\s*\})\s*$")
code_block3_pattern = re.compile(r"^\s*```")
code_block4_pattern = re.compile(r"^\s*````")


class VisibleTextExtractor(HTMLParser):
    """Extract visible text from a string with HTML tags."""

    def __init__(self):
        super().__init__()
        self.text_parts = []

    def handle_data(self, data):
        self.text_parts.append(data)

    def extract_visible_text(self, html: str) -> str:
        self.reset()
        self.text_parts = []
        self.feed(html)
        return "".join(self.text_parts).strip()


def slugify(text: str) -> str:
    return py_slugify(
        text,
        replacements=[
            ("`", ""),  # `dict`s -> dicts
            ("'s", "s"),  # it's -> its
            ("'t", "t"),  # don't -> dont
            ("**", ""),  # **FastAPI**s -> FastAPIs
        ],
    )


def get_en_config() -> dict[str, Any]:
    return mkdocs.utils.yaml_load(en_config_path.read_text(encoding="utf-8"))


def get_lang_paths() -> list[Path]:
    return sorted(docs_path.iterdir())


def lang_callback(lang: str | None) -> str | None:
    if lang is None:
        return None
    lang = lang.lower()
    return lang


def complete_existing_lang(incomplete: str):
    lang_path: Path
    for lang_path in get_lang_paths():
        if lang_path.is_dir() and lang_path.name.startswith(incomplete):
            yield lang_path.name


@app.callback()
def callback() -> None:
    # For MacOS with Cairo
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = "/opt/homebrew/lib"


@app.command()
def new_lang(lang: str = typer.Argument(..., callback=lang_callback)):
    """
    Generate a new docs translation directory for the language LANG.
    """
    new_path: Path = Path("docs") / lang
    if new_path.exists():
        typer.echo(f"The language was already created: {lang}")
        raise typer.Abort()
    new_path.mkdir()
    new_config_path: Path = Path(new_path) / mkdocs_name
    new_config_path.write_text("INHERIT: ../en/mkdocs.yml\n", encoding="utf-8")
    new_llm_prompt_path: Path = new_path / "llm-prompt.md"
    new_llm_prompt_path.write_text("", encoding="utf-8")
    print(f"Successfully initialized: {new_path}")
    update_languages()


@app.command()
def build_lang(
    lang: str = typer.Argument(
        ..., callback=lang_callback, autocompletion=complete_existing_lang
    ),
) -> None:
    """
    Build the docs for a language.
    """
    lang_path: Path = Path("docs") / lang
    if not lang_path.is_dir():
        typer.echo(f"The language translation doesn't seem to exist yet: {lang}")
        raise typer.Abort()
    typer.echo(f"Building docs for: {lang}")
    build_site_dist_path = build_site_path / lang
    if lang == "en":
        dist_path = site_path
        # Don't remove en dist_path as it might already contain other languages.
        # When running build_all(), that function already removes site_path.
        # All this is only relevant locally, on GitHub Actions all this is done through
        # artifacts and multiple workflows, so it doesn't matter if directories are
        # removed or not.
    else:
        dist_path = site_path / lang
        shutil.rmtree(dist_path, ignore_errors=True)
    current_dir = os.getcwd()
    os.chdir(lang_path)
    shutil.rmtree(build_site_dist_path, ignore_errors=True)
    subprocess.run(["mkdocs", "build", "--site-dir", build_site_dist_path], check=True)
    shutil.copytree(build_site_dist_path, dist_path, dirs_exist_ok=True)
    os.chdir(current_dir)
    typer.secho(f"Successfully built docs for: {lang}", color=typer.colors.GREEN)


index_sponsors_template = """
### Keystone Sponsor

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
### Gold and Silver Sponsors

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}

"""


def remove_header_permalinks(content: str):
    lines: list[str] = []
    for line in content.split("\n"):
        match = header_with_permalink_pattern.match(line)
        if match:
            hashes, title, *_ = match.groups()
            line = f"{hashes} {title}"
        lines.append(line)
    return "\n".join(lines)


def generate_readme_content() -> str:
    en_index = en_docs_path / "docs" / "index.md"
    content = en_index.read_text("utf-8")
    content = remove_header_permalinks(content)  # remove permalinks from headers
    match_pre = re.search(r"</style>\n\n", content)
    match_start = re.search(r"<!-- sponsors -->", content)
    match_end = re.search(r"<!-- /sponsors -->", content)
    sponsors_data_path = en_docs_path / "data" / "sponsors.yml"
    sponsors = mkdocs.utils.yaml_load(sponsors_data_path.read_text(encoding="utf-8"))
    if not (match_start and match_end):
        raise RuntimeError("Couldn't auto-generate sponsors section")
    if not match_pre:
        raise RuntimeError("Couldn't find pre section (<style>) in index.md")
    frontmatter_end = match_pre.end()
    pre_end = match_start.end()
    post_start = match_end.start()
    template = Template(index_sponsors_template)
    message = template.render(sponsors=sponsors)
    pre_content = content[frontmatter_end:pre_end]
    post_content = content[post_start:]
    new_content = pre_content + message + post_content
    # Remove content between <!-- only-mkdocs --> and <!-- /only-mkdocs -->
    new_content = re.sub(
        r"<!-- only-mkdocs -->.*?<!-- /only-mkdocs -->",
        "",
        new_content,
        flags=re.DOTALL,
    )
    return new_content


@app.command()
def generate_readme() -> None:
    """
    Generate README.md content from main index.md
    """
    readme_path = Path("README.md")
    old_content = readme_path.read_text("utf-8")
    new_content = generate_readme_content()
    if new_content != old_content:
        print("README.md outdated from the latest index.md")
        print("Updating README.md")
        readme_path.write_text(new_content, encoding="utf-8")
        raise typer.Exit(1)
    print("README.md is up to date ✅")


@app.command()
def build_all() -> None:
    """
    Build mkdocs site for en, and then build each language inside, end result is located
    at directory ./site/ with each language inside.
    """
    update_languages()
    shutil.rmtree(site_path, ignore_errors=True)
    langs = [
        lang.name
        for lang in get_lang_paths()
        if (lang.is_dir() and lang.name in SUPPORTED_LANGS)
    ]
    cpu_count = os.cpu_count() or 1
    process_pool_size = cpu_count * 4
    typer.echo(f"Using process pool size: {process_pool_size}")
    with Pool(process_pool_size) as p:
        p.map(build_lang, langs)


@app.command()
def update_languages() -> None:
    """
    Update the mkdocs.yml file Languages section including all the available languages.
    """
    old_config = get_en_config()
    updated_config = get_updated_config_content()
    if old_config != updated_config:
        print("docs/en/mkdocs.yml outdated")
        print("Updating docs/en/mkdocs.yml")
        en_config_path.write_text(
            yaml.dump(updated_config, sort_keys=False, width=200, allow_unicode=True),
            encoding="utf-8",
        )
        raise typer.Exit(1)
    print("docs/en/mkdocs.yml is up to date ✅")


@app.command()
def serve() -> None:
    """
    A quick server to preview a built site with translations.

    For development, prefer the command live (or just mkdocs serve).

    This is here only to preview a site with translations already built.

    Make sure you run the build-all command first.
    """
    typer.echo("Warning: this is a very simple server.")
    typer.echo("For development, use the command live instead.")
    typer.echo("This is here only to preview a site with translations already built.")
    typer.echo("Make sure you run the build-all command first.")
    os.chdir("site")
    server_address = ("", 8008)
    server = HTTPServer(server_address, SimpleHTTPRequestHandler)
    typer.echo("Serving at: http://127.0.0.1:8008")
    server.serve_forever()


@app.command()
def live(
    lang: str = typer.Argument(
        None, callback=lang_callback, autocompletion=complete_existing_lang
    ),
    dirty: bool = False,
) -> None:
    """
    Serve with livereload a docs site for a specific language.

    This only shows the actual translated files, not the placeholders created with
    build-all.

    Takes an optional LANG argument with the name of the language to serve, by default
    en.
    """
    # Enable line numbers during local development to make it easier to highlight
    if lang is None:
        lang = "en"
    lang_path: Path = docs_path / lang
    # Enable line numbers during local development to make it easier to highlight
    args = ["mkdocs", "serve", "--dev-addr", "127.0.0.1:8008"]
    if dirty:
        args.append("--dirty")
    subprocess.run(
        args, env={**os.environ, "LINENUMS": "true"}, cwd=lang_path, check=True
    )


def get_updated_config_content() -> dict[str, Any]:
    config = get_en_config()
    languages = [{"en": "/"}]
    new_alternate: list[dict[str, str]] = []
    # Language names sourced from https://quickref.me/iso-639-1
    # Contributors may wish to update or change these, e.g. to fix capitalization.
    language_names_path = Path(__file__).parent / "../docs/language_names.yml"
    local_language_names: dict[str, str] = mkdocs.utils.yaml_load(
        language_names_path.read_text(encoding="utf-8")
    )
    for lang_path in get_lang_paths():
        if lang_path.name in {"en", "em"} or not lang_path.is_dir():
            continue
        if lang_path.name not in SUPPORTED_LANGS:
            # Skip languages that are not yet ready
            continue
        code = lang_path.name
        languages.append({code: f"/{code}/"})
    for lang_dict in languages:
        code = list(lang_dict.keys())[0]
        url = lang_dict[code]
        if code not in local_language_names:
            print(
                f"Missing language name for: {code}, "
                "update it in docs/language_names.yml"
            )
            raise typer.Abort()
        use_name = f"{code} - {local_language_names[code]}"
        new_alternate.append({"link": url, "name": use_name})
    config["extra"]["alternate"] = new_alternate
    return config


@app.command()
def ensure_non_translated() -> None:
    """
    Ensure there are no files in the non translatable pages.
    """
    print("Ensuring no non translated pages")
    lang_paths = get_lang_paths()
    error_paths = []
    for lang in lang_paths:
        if lang.name == "en":
            continue
        for non_translatable in non_translated_sections:
            non_translatable_path = lang / "docs" / non_translatable
            if non_translatable_path.exists():
                error_paths.append(non_translatable_path)
    if error_paths:
        print("Non-translated pages found, removing them:")
        for error_path in error_paths:
            print(error_path)
            if error_path.is_file():
                error_path.unlink()
            else:
                shutil.rmtree(error_path)
        raise typer.Exit(1)
    print("No non-translated pages found ✅")


@app.command()
def langs_json():
    langs = []
    for lang_path in get_lang_paths():
        if lang_path.is_dir() and lang_path.name in SUPPORTED_LANGS:
            langs.append(lang_path.name)
    print(json.dumps(langs))


@app.command()
def generate_docs_src_versions_for_file(file_path: Path) -> None:
    target_versions = ["py39", "py310"]
    full_path_str = str(file_path)
    for target_version in target_versions:
        if f"_{target_version}" in full_path_str:
            logging.info(
                f"Skipping {file_path}, already a version file for {target_version}"
            )
            return
    base_content = file_path.read_text(encoding="utf-8")
    previous_content = {base_content}
    for target_version in target_versions:
        version_result = subprocess.run(
            [
                find_ruff_bin(),
                "check",
                "--target-version",
                target_version,
                "--fix",
                "--unsafe-fixes",
                "-",
            ],
            input=base_content.encode("utf-8"),
            capture_output=True,
        )
        content_target = version_result.stdout.decode("utf-8")
        format_result = subprocess.run(
            [find_ruff_bin(), "format", "-"],
            input=content_target.encode("utf-8"),
            capture_output=True,
        )
        content_format = format_result.stdout.decode("utf-8")
        if content_format in previous_content:
            continue
        previous_content.add(content_format)
        # Determine where the version label should go: in the parent directory
        # name or in the file name, matching the source structure.
        label_in_parent = False
        for v in target_versions:
            if f"_{v}" in file_path.parent.name:
                label_in_parent = True
                break
        if label_in_parent:
            parent_name = file_path.parent.name
            for v in target_versions:
                parent_name = parent_name.replace(f"_{v}", "")
            new_parent = file_path.parent.parent / f"{parent_name}_{target_version}"
            new_parent.mkdir(parents=True, exist_ok=True)
            version_file = new_parent / file_path.name
        else:
            base_name = file_path.stem
            for v in target_versions:
                if base_name.endswith(f"_{v}"):
                    base_name = base_name[: -len(f"_{v}")]
                    break
            version_file = file_path.with_name(f"{base_name}_{target_version}.py")
        logging.info(f"Writing to {version_file}")
        version_file.write_text(content_format, encoding="utf-8")


@app.command()
def generate_docs_src_versions() -> None:
    """
    Generate Python version-specific files for all .py files in docs_src.
    """
    docs_src_path = Path("docs_src")
    for py_file in sorted(docs_src_path.rglob("*.py")):
        generate_docs_src_versions_for_file(py_file)


@app.command()
def copy_py39_to_py310() -> None:
    """
    For each docs_src file/directory with a _py39 label that has no _py310
    counterpart, copy it with the _py310 label.
    """
    docs_src_path = Path("docs_src")
    # Handle directory-level labels (e.g. app_b_an_py39/)
    for dir_path in sorted(docs_src_path.rglob("*_py39")):
        if not dir_path.is_dir():
            continue
        py310_dir = dir_path.parent / dir_path.name.replace("_py39", "_py310")
        if py310_dir.exists():
            continue
        logging.info(f"Copying directory {dir_path} -> {py310_dir}")
        shutil.copytree(dir_path, py310_dir)
    # Handle file-level labels (e.g. tutorial001_py39.py)
    for file_path in sorted(docs_src_path.rglob("*_py39.py")):
        if not file_path.is_file():
            continue
        # Skip files inside _py39 directories (already handled above)
        if "_py39" in file_path.parent.name:
            continue
        py310_file = file_path.with_name(
            file_path.name.replace("_py39.py", "_py310.py")
        )
        if py310_file.exists():
            continue
        logging.info(f"Copying file {file_path} -> {py310_file}")
        shutil.copy2(file_path, py310_file)


@app.command()
def update_docs_includes_py39_to_py310() -> None:
    """
    Update .md files in docs/en/ to replace _py39 includes with _py310 versions.

    For each include line referencing a _py39 file or directory in docs_src, replace
    the _py39 label with _py310.
    """
    include_pattern = re.compile(r"\{[^}]*docs_src/[^}]*_py39[^}]*\.py[^}]*\}")
    count = 0
    for md_file in sorted(en_docs_path.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        if "_py39" not in content:
            continue
        new_content = include_pattern.sub(
            lambda m: m.group(0).replace("_py39", "_py310"), content
        )
        if new_content != content:
            md_file.write_text(new_content, encoding="utf-8")
            count += 1
            logging.info(f"Updated includes in {md_file}")
    print(f"Updated {count} file(s) ✅")


@app.command()
def remove_unused_docs_src() -> None:
    """
    Delete .py files in docs_src that are not included in any .md file under docs/.
    """
    docs_src_path = Path("docs_src")
    # Collect all docs .md content referencing docs_src
    all_docs_content = ""
    for md_file in docs_path.rglob("*.md"):
        all_docs_content += md_file.read_text(encoding="utf-8")
    # Build a set of directory-based package roots (e.g. docs_src/bigger_applications/app_py39)
    # where at least one file is referenced in docs. All files in these directories
    # should be kept since they may be internally imported by the referenced files.
    used_package_dirs: set[Path] = set()
    for py_file in docs_src_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        rel_path = str(py_file)
        if rel_path in all_docs_content:
            # Walk up from the file's parent to find the package root
            # (a subdirectory under docs_src/<topic>/)
            parts = py_file.relative_to(docs_src_path).parts
            if len(parts) > 2:
                # File is inside a sub-package like docs_src/topic/app_xxx/...
                package_root = docs_src_path / parts[0] / parts[1]
                used_package_dirs.add(package_root)
    removed = 0
    for py_file in sorted(docs_src_path.rglob("*.py")):
        if py_file.name == "__init__.py":
            continue
        # Build the relative path as it appears in includes (e.g. docs_src/first_steps/tutorial001.py)
        rel_path = str(py_file)
        if rel_path in all_docs_content:
            continue
        # If this file is inside a directory-based package where any sibling is
        # referenced, keep it (it's likely imported internally).
        parts = py_file.relative_to(docs_src_path).parts
        if len(parts) > 2:
            package_root = docs_src_path / parts[0] / parts[1]
            if package_root in used_package_dirs:
                continue
        # Check if the _an counterpart (or non-_an counterpart) is referenced.
        # If either variant is included, keep both.
        # Handle both file-level _an (tutorial001_an.py) and directory-level _an
        # (app_an/main.py)
        counterpart_found = False
        full_path_str = str(py_file)
        if "_an" in py_file.stem:
            # This is an _an file, check if the non-_an version is referenced
            counterpart = full_path_str.replace(
                f"/{py_file.stem}", f"/{py_file.stem.replace('_an', '', 1)}"
            )
            if counterpart in all_docs_content:
                counterpart_found = True
        else:
            # This is a non-_an file, check if there's an _an version referenced
            # Insert _an before any version suffix or at the end of the stem
            stem = py_file.stem
            for suffix in ("_py39", "_py310"):
                if suffix in stem:
                    an_stem = stem.replace(suffix, f"_an{suffix}", 1)
                    break
            else:
                an_stem = f"{stem}_an"
            counterpart = full_path_str.replace(f"/{stem}.", f"/{an_stem}.")
            if counterpart in all_docs_content:
                counterpart_found = True
        # Also check directory-level _an counterparts
        if not counterpart_found:
            parent_name = py_file.parent.name
            if "_an" in parent_name:
                counterpart_parent = parent_name.replace("_an", "", 1)
                counterpart_dir = str(py_file).replace(
                    f"/{parent_name}/", f"/{counterpart_parent}/"
                )
                if counterpart_dir in all_docs_content:
                    counterpart_found = True
            else:
                # Try inserting _an into parent directory name
                for suffix in ("_py39", "_py310"):
                    if suffix in parent_name:
                        an_parent = parent_name.replace(suffix, f"_an{suffix}", 1)
                        break
                else:
                    an_parent = f"{parent_name}_an"
                counterpart_dir = str(py_file).replace(
                    f"/{parent_name}/", f"/{an_parent}/"
                )
                if counterpart_dir in all_docs_content:
                    counterpart_found = True
        if counterpart_found:
            continue
        logging.info(f"Removing unused file: {py_file}")
        py_file.unlink()
        removed += 1
    # Clean up directories that are empty or only contain __init__.py / __pycache__
    for dir_path in sorted(docs_src_path.rglob("*"), reverse=True):
        if not dir_path.is_dir():
            continue
        remaining = [
            f
            for f in dir_path.iterdir()
            if f.name != "__pycache__" and f.name != "__init__.py"
        ]
        if not remaining:
            logging.info(f"Removing empty/init-only directory: {dir_path}")
            shutil.rmtree(dir_path)
    print(f"Removed {removed} unused file(s) ✅")


@app.command()
def add_permalinks_page(path: Path, update_existing: bool = False):
    """
    Add or update header permalinks in specific page of En docs.
    """

    if not path.is_relative_to(en_docs_path / "docs"):
        raise RuntimeError(f"Path must be inside {en_docs_path}")
    rel_path = path.relative_to(en_docs_path / "docs")

    # Skip excluded sections
    if str(rel_path).startswith(non_translated_sections):
        return

    visible_text_extractor = VisibleTextExtractor()
    updated_lines = []
    in_code_block3 = False
    in_code_block4 = False
    permalinks = set()

    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        # Handle codeblocks start and end
        if not (in_code_block3 or in_code_block4):
            if code_block4_pattern.match(line):
                in_code_block4 = True
            elif code_block3_pattern.match(line):
                in_code_block3 = True
        else:
            if in_code_block4 and code_block4_pattern.match(line):
                in_code_block4 = False
            elif in_code_block3 and code_block3_pattern.match(line):
                in_code_block3 = False

        # Process Headers only outside codeblocks
        if not (in_code_block3 or in_code_block4):
            match = header_pattern.match(line)
            if match:
                hashes, title, _permalink = match.groups()
                if (not _permalink) or update_existing:
                    slug = slugify(visible_text_extractor.extract_visible_text(title))
                    if slug in permalinks:
                        # If the slug is already used, append a number to make it unique
                        count = 1
                        original_slug = slug
                        while slug in permalinks:
                            slug = f"{original_slug}_{count}"
                            count += 1
                    permalinks.add(slug)

                    line = f"{hashes} {title} {{ #{slug} }}\n"

        updated_lines.append(line)

    with path.open("w", encoding="utf-8") as f:
        f.writelines(updated_lines)


@app.command()
def add_permalinks_pages(pages: list[Path], update_existing: bool = False) -> None:
    """
    Add or update header permalinks in specific pages of En docs.
    """
    for md_file in pages:
        add_permalinks_page(md_file, update_existing=update_existing)


@app.command()
def add_permalinks(update_existing: bool = False) -> None:
    """
    Add or update header permalinks in all pages of En docs.
    """
    for md_file in en_docs_path.rglob("*.md"):
        add_permalinks_page(md_file, update_existing=update_existing)


if __name__ == "__main__":
    app()
