import os
import re
import shutil
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Pool
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import mkdocs.commands.build
import mkdocs.commands.serve
import mkdocs.config
import mkdocs.utils
import typer
import yaml
from jinja2 import Template

app = typer.Typer()

mkdocs_name = "mkdocs.yml"

missing_translation_snippet = """
{!../../../docs/missing-translation.md!}
"""

docs_path = Path("docs")
en_docs_path = Path("docs/en")
en_config_path: Path = en_docs_path / mkdocs_name


def get_en_config() -> dict:
    return mkdocs.utils.yaml_load(en_config_path.read_text(encoding="utf-8"))


def get_lang_paths():
    return sorted(docs_path.iterdir())


def lang_callback(lang: Optional[str]):
    if lang is None:
        return
    if not lang.isalpha() or len(lang) != 2:
        typer.echo("Use a 2 letter language code, like: es")
        raise typer.Abort()
    lang = lang.lower()
    return lang


def complete_existing_lang(incomplete: str):
    lang_path: Path
    for lang_path in get_lang_paths():
        if lang_path.is_dir() and lang_path.name.startswith(incomplete):
            yield lang_path.name


def get_base_lang_config(lang: str):
    en_config = get_en_config()
    fastapi_url_base = "https://fastapi.tiangolo.com/"
    new_config = en_config.copy()
    new_config["site_url"] = en_config["site_url"] + f"{lang}/"
    new_config["theme"]["logo"] = fastapi_url_base + en_config["theme"]["logo"]
    new_config["theme"]["favicon"] = fastapi_url_base + en_config["theme"]["favicon"]
    new_config["theme"]["language"] = lang
    new_config["nav"] = en_config["nav"][:2]
    extra_css = []
    css: str
    for css in en_config["extra_css"]:
        if css.startswith("http"):
            extra_css.append(css)
        else:
            extra_css.append(fastapi_url_base + css)
    new_config["extra_css"] = extra_css

    extra_js = []
    js: str
    for js in en_config["extra_javascript"]:
        if js.startswith("http"):
            extra_js.append(js)
        else:
            extra_js.append(fastapi_url_base + js)
    new_config["extra_javascript"] = extra_js
    return new_config


@app.command()
def new_lang(lang: str = typer.Argument(..., callback=lang_callback)):
    """
    Generate a new docs translation directory for the language LANG.

    LANG should be a 2-letter language code, like: en, es, de, pt, etc.
    """
    new_path: Path = Path("docs") / lang
    if new_path.exists():
        typer.echo(f"The language was already created: {lang}")
        raise typer.Abort()
    new_path.mkdir()
    new_config = get_base_lang_config(lang)
    new_config_path: Path = Path(new_path) / mkdocs_name
    new_config_path.write_text(
        yaml.dump(new_config, sort_keys=False, width=200, allow_unicode=True),
        encoding="utf-8",
    )
    new_config_docs_path: Path = new_path / "docs"
    new_config_docs_path.mkdir()
    en_index_path: Path = en_docs_path / "docs" / "index.md"
    new_index_path: Path = new_config_docs_path / "index.md"
    en_index_content = en_index_path.read_text(encoding="utf-8")
    new_index_content = f"{missing_translation_snippet}\n\n{en_index_content}"
    new_index_path.write_text(new_index_content, encoding="utf-8")
    new_overrides_gitignore_path = new_path / "overrides" / ".gitignore"
    new_overrides_gitignore_path.parent.mkdir(parents=True, exist_ok=True)
    new_overrides_gitignore_path.write_text("")
    typer.secho(f"Successfully initialized: {new_path}", color=typer.colors.GREEN)
    update_languages(lang=None)


@app.command()
def build_lang(
    lang: str = typer.Argument(
        ..., callback=lang_callback, autocompletion=complete_existing_lang
    )
):
    """
    Build the docs for a language, filling missing pages with translation notifications.
    """
    lang_path: Path = Path("docs") / lang
    if not lang_path.is_dir():
        typer.echo(f"The language translation doesn't seem to exist yet: {lang}")
        raise typer.Abort()
    typer.echo(f"Building docs for: {lang}")
    build_dir_path = Path("docs_build")
    build_dir_path.mkdir(exist_ok=True)
    build_lang_path = build_dir_path / lang
    en_lang_path = Path("docs/en")
    site_path = Path("site").absolute()
    if lang == "en":
        dist_path = site_path
    else:
        dist_path: Path = site_path / lang
    shutil.rmtree(build_lang_path, ignore_errors=True)
    shutil.copytree(lang_path, build_lang_path)
    shutil.copytree(en_docs_path / "data", build_lang_path / "data")
    overrides_src = en_docs_path / "overrides"
    overrides_dest = build_lang_path / "overrides"
    for path in overrides_src.iterdir():
        dest_path = overrides_dest / path.name
        if not dest_path.exists():
            shutil.copy(path, dest_path)
    en_config_path: Path = en_lang_path / mkdocs_name
    en_config: dict = mkdocs.utils.yaml_load(en_config_path.read_text(encoding="utf-8"))
    nav = en_config["nav"]
    lang_config_path: Path = lang_path / mkdocs_name
    lang_config: dict = mkdocs.utils.yaml_load(
        lang_config_path.read_text(encoding="utf-8")
    )
    lang_nav = lang_config["nav"]
    # Exclude first 2 entries FastAPI and Languages, for custom handling
    use_nav = nav[2:]
    lang_use_nav = lang_nav[2:]
    file_to_nav = get_file_to_nav_map(use_nav)
    sections = get_sections(use_nav)
    lang_file_to_nav = get_file_to_nav_map(lang_use_nav)
    use_lang_file_to_nav = get_file_to_nav_map(lang_use_nav)
    for file in file_to_nav:
        file_path = Path(file)
        lang_file_path: Path = build_lang_path / "docs" / file_path
        en_file_path: Path = en_lang_path / "docs" / file_path
        lang_file_path.parent.mkdir(parents=True, exist_ok=True)
        if not lang_file_path.is_file():
            en_text = en_file_path.read_text(encoding="utf-8")
            lang_text = get_text_with_translate_missing(en_text)
            lang_file_path.write_text(lang_text, encoding="utf-8")
            file_key = file_to_nav[file]
            use_lang_file_to_nav[file] = file_key
            if file_key:
                composite_key = ()
                new_key = ()
                for key_part in file_key:
                    composite_key += (key_part,)
                    key_first_file = sections[composite_key]
                    if key_first_file in lang_file_to_nav:
                        new_key = lang_file_to_nav[key_first_file]
                    else:
                        new_key += (key_part,)
                use_lang_file_to_nav[file] = new_key
    key_to_section = {(): []}
    for file, orig_file_key in file_to_nav.items():
        if file in use_lang_file_to_nav:
            file_key = use_lang_file_to_nav[file]
        else:
            file_key = orig_file_key
        section = get_key_section(key_to_section=key_to_section, key=file_key)
        section.append(file)
    new_nav = key_to_section[()]
    export_lang_nav = [lang_nav[0], nav[1]] + new_nav
    lang_config["nav"] = export_lang_nav
    build_lang_config_path: Path = build_lang_path / mkdocs_name
    build_lang_config_path.write_text(
        yaml.dump(lang_config, sort_keys=False, width=200, allow_unicode=True),
        encoding="utf-8",
    )
    current_dir = os.getcwd()
    os.chdir(build_lang_path)
    subprocess.run(["mkdocs", "build", "--site-dir", dist_path], check=True)
    os.chdir(current_dir)
    typer.secho(f"Successfully built docs for: {lang}", color=typer.colors.GREEN)


index_sponsors_template = """
{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}
"""


def generate_readme_content():
    en_index = en_docs_path / "docs" / "index.md"
    content = en_index.read_text("utf-8")
    match_start = re.search(r"<!-- sponsors -->", content)
    match_end = re.search(r"<!-- /sponsors -->", content)
    sponsors_data_path = en_docs_path / "data" / "sponsors.yml"
    sponsors = mkdocs.utils.yaml_load(sponsors_data_path.read_text(encoding="utf-8"))
    if not (match_start and match_end):
        raise RuntimeError("Couldn't auto-generate sponsors section")
    pre_end = match_start.end()
    post_start = match_end.start()
    template = Template(index_sponsors_template)
    message = template.render(sponsors=sponsors)
    pre_content = content[:pre_end]
    post_content = content[post_start:]
    new_content = pre_content + message + post_content
    return new_content


@app.command()
def generate_readme():
    """
    Generate README.md content from main index.md
    """
    typer.echo("Generating README")
    readme_path = Path("README.md")
    new_content = generate_readme_content()
    readme_path.write_text(new_content, encoding="utf-8")


@app.command()
def verify_readme():
    """
    Verify README.md content from main index.md
    """
    typer.echo("Verifying README")
    readme_path = Path("README.md")
    generated_content = generate_readme_content()
    readme_content = readme_path.read_text("utf-8")
    if generated_content != readme_content:
        typer.secho(
            "README.md outdated from the latest index.md", color=typer.colors.RED
        )
        raise typer.Abort()
    typer.echo("Valid README ✅")


@app.command()
def build_all():
    """
    Build mkdocs site for en, and then build each language inside, end result is located
    at directory ./site/ with each language inside.
    """
    site_path = Path("site").absolute()
    update_languages(lang=None)
    current_dir = os.getcwd()
    os.chdir(en_docs_path)
    typer.echo("Building docs for: en")
    subprocess.run(["mkdocs", "build", "--site-dir", site_path], check=True)
    os.chdir(current_dir)
    langs = []
    for lang in get_lang_paths():
        if lang == en_docs_path or not lang.is_dir():
            continue
        langs.append(lang.name)
    cpu_count = os.cpu_count() or 1
    with Pool(cpu_count * 2) as p:
        p.map(build_lang, langs)


def update_single_lang(lang: str):
    lang_path = docs_path / lang
    typer.echo(f"Updating {lang_path.name}")
    update_config(lang_path.name)


@app.command()
def update_languages(
    lang: str = typer.Argument(
        None, callback=lang_callback, autocompletion=complete_existing_lang
    )
):
    """
    Update the mkdocs.yml file Languages section including all the available languages.

    The LANG argument is a 2-letter language code. If it's not provided, update all the
    mkdocs.yml files (for all the languages).
    """
    if lang is None:
        for lang_path in get_lang_paths():
            if lang_path.is_dir():
                update_single_lang(lang_path.name)
    else:
        update_single_lang(lang)


@app.command()
def serve():
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
    typer.echo(f"Serving at: http://127.0.0.1:8008")
    server.serve_forever()


@app.command()
def live(
    lang: str = typer.Argument(
        None, callback=lang_callback, autocompletion=complete_existing_lang
    )
):
    """
    Serve with livereload a docs site for a specific language.

    This only shows the actual translated files, not the placeholders created with
    build-all.

    Takes an optional LANG argument with the name of the language to serve, by default
    en.
    """
    if lang is None:
        lang = "en"
    lang_path: Path = docs_path / lang
    os.chdir(lang_path)
    mkdocs.commands.serve.serve(dev_addr="127.0.0.1:8008")


def update_config(lang: str):
    lang_path: Path = docs_path / lang
    config_path = lang_path / mkdocs_name
    current_config: dict = mkdocs.utils.yaml_load(
        config_path.read_text(encoding="utf-8")
    )
    if lang == "en":
        config = get_en_config()
    else:
        config = get_base_lang_config(lang)
        config["nav"] = current_config["nav"]
        config["theme"]["language"] = current_config["theme"]["language"]
    languages = [{"en": "/"}]
    alternate: List[Dict[str, str]] = config["extra"].get("alternate", [])
    alternate_dict = {alt["link"]: alt["name"] for alt in alternate}
    new_alternate: List[Dict[str, str]] = []
    for lang_path in get_lang_paths():
        if lang_path.name == "en" or not lang_path.is_dir():
            continue
        name = lang_path.name
        languages.append({name: f"/{name}/"})
    for lang_dict in languages:
        name = list(lang_dict.keys())[0]
        url = lang_dict[name]
        if url not in alternate_dict:
            new_alternate.append({"link": url, "name": name})
        else:
            use_name = alternate_dict[url]
            new_alternate.append({"link": url, "name": use_name})
    config["nav"][1] = {"Languages": languages}
    config["extra"]["alternate"] = new_alternate
    config_path.write_text(
        yaml.dump(config, sort_keys=False, width=200, allow_unicode=True),
        encoding="utf-8",
    )


def get_key_section(
    *, key_to_section: Dict[Tuple[str, ...], list], key: Tuple[str, ...]
) -> list:
    if key in key_to_section:
        return key_to_section[key]
    super_key = key[:-1]
    title = key[-1]
    super_section = get_key_section(key_to_section=key_to_section, key=super_key)
    new_section = []
    super_section.append({title: new_section})
    key_to_section[key] = new_section
    return new_section


def get_text_with_translate_missing(text: str) -> str:
    lines = text.splitlines()
    lines.insert(1, missing_translation_snippet)
    new_text = "\n".join(lines)
    return new_text


def get_file_to_nav_map(nav: list) -> Dict[str, Tuple[str, ...]]:
    file_to_nav = {}
    for item in nav:
        if type(item) is str:
            file_to_nav[item] = tuple()
        elif type(item) is dict:
            item_key = list(item.keys())[0]
            sub_nav = item[item_key]
            sub_file_to_nav = get_file_to_nav_map(sub_nav)
            for k, v in sub_file_to_nav.items():
                file_to_nav[k] = (item_key,) + v
    return file_to_nav


def get_sections(nav: list) -> Dict[Tuple[str, ...], str]:
    sections = {}
    for item in nav:
        if type(item) is str:
            continue
        elif type(item) is dict:
            item_key = list(item.keys())[0]
            sub_nav = item[item_key]
            sections[(item_key,)] = sub_nav[0]
            sub_sections = get_sections(sub_nav)
            for k, v in sub_sections.items():
                new_key = (item_key,) + k
                sections[new_key] = v
    return sections


if __name__ == "__main__":
    app()
