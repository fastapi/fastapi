"""
FastAPI Documentation Management Script.

This script provides a comprehensive set of commands for managing multi-language
documentation for FastAPI. It handles building, serving, verifying, and maintaining
documentation across multiple languages.

Key features:
- Building documentation for individual languages or all languages
- Generating and verifying README content
- Managing language configurations
- Serving documentation for development
- Verifying documentation integrity

The script uses Typer for CLI interface and supports parallel processing for
efficient builds.
"""

import json
import logging
import os
import re
import shutil
import subprocess
from functools import lru_cache
from http.server import HTTPServer, SimpleHTTPRequestHandler
from importlib import metadata
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import mkdocs.utils
import typer
import yaml
from jinja2 import Template
from ruff.__main__ import find_ruff_bin

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Typer app
app = typer.Typer()

# Constants
mkdocs_name = "mkdocs.yml"
missing_translation_snippet = """
{!../../docs/missing-translation.md!}
"""

# Sections that should not be translated
non_translated_sections = [
    "reference/",
    "release-notes.md",
    "fastapi-people.md",
    "external-links.md",
    "newsletter.md",
    "management-tasks.md",
    "management.md",
    "contributing.md",
]

# Path configurations
docs_path = Path("docs")
en_docs_path = Path("docs/en")
en_config_path: Path = en_docs_path / mkdocs_name
site_path = Path("site").absolute()
build_site_path = Path("site_build").absolute()

# Regex pattern for header permalinks
header_with_permalink_pattern = re.compile(r"^(#{1,6}) (.+?)(\s*\{\s*#.*\s*\})\s*$")


@lru_cache
def is_mkdocs_insiders() -> bool:
    """
    Check if mkdocs-material insiders version is installed.
    
    Returns:
        bool: True if insiders version is detected, False otherwise
    """
    version = metadata.version("mkdocs-material")
    return "insiders" in version


def get_en_config() -> Dict[str, Any]:
    """
    Load and parse the English documentation configuration file.
    
    Returns:
        Dict[str, Any]: Parsed YAML content from mkdocs.yml
    """
    return mkdocs.utils.yaml_load(en_config_path.read_text(encoding="utf-8"))


def get_lang_paths() -> List[Path]:
    """
    Get all language directory paths from the docs directory.
    
    Returns:
        List[Path]: Sorted list of Path objects for each language directory
    """
    return sorted(docs_path.iterdir())


def lang_callback(lang: Optional[str]) -> Union[str, None]:
    """
    Typer callback function to normalize language input.
    
    Args:
        lang: Language code to normalize
        
    Returns:
        Normalized lowercase language code or None if input is None
    """
    if lang is None:
        return None
    lang = lang.lower()
    return lang


def complete_existing_lang(incomplete: str):
    """
    Autocomplete function for existing languages.
    
    Args:
        incomplete: Partial language name to complete
        
    Yields:
        str: Matching language directory names
    """
    lang_path: Path
    for lang_path in get_lang_paths():
        if lang_path.is_dir() and lang_path.name.startswith(incomplete):
            yield lang_path.name


@app.callback()
def callback() -> None:
    """
    Global callback function executed before any command.
    
    Sets up environment variables for mkdocs-insiders and MacOS Cairo support.
    """
    if is_mkdocs_insiders():
        os.environ["INSIDERS_FILE"] = "../en/mkdocs.insiders.yml"
    # For MacOS with insiders and Cairo
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = "/opt/homebrew/lib"


@app.command()
def new_lang(lang: str = typer.Argument(..., callback=lang_callback)):
    """
    Generate a new docs translation directory for the specified language.
    
    Creates the necessary directory structure, configuration file, and initial
    content for a new language translation.
    
    Args:
        lang: Language code for the new translation (e.g., 'es', 'fr')
        
    Raises:
        typer.Abort: If the language directory already exists
    """
    new_path: Path = Path("docs") / lang
    if new_path.exists():
        typer.echo(f"The language was already created: {lang}")
        raise typer.Abort()
    new_path.mkdir()
    new_config_path: Path = Path(new_path) / mkdocs_name
    new_config_path.write_text("INHERIT: ../en/mkdocs.yml\n", encoding="utf-8")
    new_config_docs_path: Path = new_path / "docs"
    new_config_docs_path.mkdir()
    en_index_path: Path = en_docs_path / "docs" / "index.md"
    new_index_path: Path = new_config_docs_path / "index.md"
    en_index_content = en_index_path.read_text(encoding="utf-8")
    new_index_content = f"{missing_translation_snippet}\n\n{en_index_content}"
    new_index_path.write_text(new_index_content, encoding="utf-8")
    typer.secho(f"Successfully initialized: {new_path}", color=typer.colors.GREEN)
    update_languages()


@app.command()
def build_lang(
    lang: str = typer.Argument(
        ..., callback=lang_callback, autocompletion=complete_existing_lang
    ),
) -> None:
    """
    Build the documentation for a specific language.
    
    Uses mkdocs to build the documentation site for the specified language
    and copies the output to the appropriate location.
    
    Args:
        lang: Language code to build (e.g., 'en', 'es')
        
    Raises:
        typer.Abort: If the language directory doesn't exist
    """
    insiders_env_file = os.environ.get("INSIDERS_FILE")
    print(f"Insiders file {insiders_env_file}")
    if is_mkdocs_insiders():
        print("Using insiders")
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


# Template for sponsors section in README
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


def remove_header_permalinks(content: str) -> str:
    """
    Remove permalinks from markdown headers.
    
    Args:
        content: Markdown content with header permalinks
        
    Returns:
        str: Markdown content with permalinks removed from headers
    """
    lines: list[str] = []
    for line in content.split("\n"):
        match = header_with_permalink_pattern.match(line)
        if match:
            hashes, title, *_ = match.groups()
            line = f"{hashes} {title}"
        lines.append(line)
    return "\n".join(lines)


def generate_readme_content() -> str:
    """
    Generate README.md content from the main English index.md file.
    
    Processes the index.md file to remove mkdocs-specific elements and
    generates appropriate content for GitHub README.
    
    Returns:
        str: Generated README content
        
    Raises:
        RuntimeError: If required sections are not found in the source content
    """
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
    Generate README.md file from the main English documentation index.md.
    
    This command processes the main documentation index file to create
    a GitHub-appropriate README with sponsors information and without
    mkdocs-specific elements.
    """
    typer.echo("Generating README")
    readme_path = Path("README.md")
    new_content = generate_readme_content()
    readme_path.write_text(new_content, encoding="utf-8")


@app.command()
def verify_readme() -> None:
    """
    Verify that README.md is up-to-date with the main documentation index.
    
    Compares the current README content with what would be generated
    from the main index.md file and reports any discrepancies.
    
    Raises:
        typer.Abort: If README.md is outdated
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
def build_all() -> None:
    """
    Build documentation for all available languages.
    
    This command:
    1. Updates language configurations
    2. Cleans the output directory
    3. Builds documentation for all languages in parallel
    4. Places the final output in the site/ directory
    
    Uses multiprocessing for efficient parallel builds across all CPU cores.
    """
    update_languages()
    shutil.rmtree(site_path, ignore_errors=True)
    langs = [lang.name for lang in get_lang_paths() if lang.is_dir()]
    cpu_count = os.cpu_count() or 1
    process_pool_size = cpu_count * 4
    typer.echo(f"Using process pool size: {process_pool_size}")
    with Pool(process_pool_size) as p:
        p.map(build_lang, langs)


@app.command()
def update_languages() -> None:
    """
    Update the mkdocs.yml file with all available languages.
    
    This command regenerates the language configuration section in the
    main mkdocs.yml file to include all currently available translations.
    """
    update_config()


@app.command()
def serve() -> None:
    """
    Start a simple HTTP server to preview the built documentation site.
    
    This is a basic server for previewing the complete built site with
    all translations. For development, use the 'live' command instead.
    
    Note: Requires running 'build-all' first to generate the site.
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
    Serve documentation with live reload for a specific language.
    
    This command starts a mkdocs development server with livereload
    functionality for real-time preview during documentation development.
    
    Args:
        lang: Language to serve (defaults to 'en' if not specified)
        dirty: Use dirty build mode for faster rebuilds
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


def get_updated_config_content() -> Dict[str, Any]:
    """
    Generate updated mkdocs configuration with all available languages.
    
    Reads the language names from language_names.yml and generates the
    complete alternate language configuration for the mkdocs.yml file.
    
    Returns:
        Dict[str, Any]: Updated mkdocs configuration with all languages
        
    Raises:
        typer.Abort: If a language code is missing from language_names.yml
    """
    config = get_en_config()
    languages = [{"en": "/"}]
    new_alternate: List[Dict[str, str]] = []
    # Language names sourced from https://quickref.me/iso-639-1
    # Contributors may wish to update or change these, e.g. to fix capitalization.
    language_names_path = Path(__file__).parent / "../docs/language_names.yml"
    local_language_names: Dict[str, str] = mkdocs.utils.yaml_load(
        language_names_path.read_text(encoding="utf-8")
    )
    for lang_path in get_lang_paths():
        if lang_path.name in {"en", "em"} or not lang_path.is_dir():
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
    new_alternate.append({"link": "/em/", "name": "😉"})
    config["extra"]["alternate"] = new_alternate
    return config


def update_config() -> None:
    """
    Update the main English mkdocs.yml file with current language configuration.
    
    Writes the updated configuration generated by get_updated_config_content()
    back to the mkdocs.yml file.
    """
    config = get_updated_config_content()
    en_config_path.write_text(
        yaml.dump(config, sort_keys=False, width=200, allow_unicode=True),
        encoding="utf-8",
    )


@app.command()
def verify_config() -> None:
    """
    Verify that mkdocs.yml is up-to-date with language names.
    
    Checks if the current mkdocs.yml configuration matches what would be
    generated from the current language_names.yml file.
    
    Raises:
        typer.Abort: If mkdocs.yml is outdated
    """
    typer.echo("Verifying mkdocs.yml")
    config = get_en_config()
    updated_config = get_updated_config_content()
    if config != updated_config:
        typer.secho(
            "docs/en/mkdocs.yml outdated from docs/language_names.yml, "
            "update language_names.yml and run "
            "python ./scripts/docs.py update-languages",
            color=typer.colors.RED,
        )
        raise typer.Abort()
    typer.echo("Valid mkdocs.yml ✅")


@app.command()
def verify_non_translated() -> None:
    """
    Verify that non-translatable sections don't exist in translation directories.
    
    Checks all language directories (except English) to ensure they don't
    contain files or directories that are marked as non-translatable.
    
    Raises:
        typer.Abort: If non-translatable content is found in translation directories
    """
    print("Verifying non translated pages")
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
        print("Non-translated pages found, remove them:")
        for error_path in error_paths:
            print(error_path)
        raise typer.Abort()
    print("No non-translated pages found ✅")


@app.command()
def verify_docs() -> None:
    """
    Run all documentation verification checks.
    
    This command runs a comprehensive verification including:
    - README.md validation
    - mkdocs.yml configuration validation
    - Non-translated content validation
    
    This is useful as a pre-commit or CI check to ensure documentation integrity.
    """
    verify_readme()
    verify_config()
    verify_non_translated()


@app.command()
def langs_json() -> None:
    """
    Output all available language codes as JSON.
    
    Prints a JSON array containing all available language codes found
    in the docs directory. Useful for scripting and automation.
    """
    langs = []
    for lang_path in get_lang_paths():
        if lang_path.is_dir():
            langs.append(lang_path.name)
    print(json.dumps(langs))


@app.command()
def generate_docs_src_versions_for_file(file_path: Path) -> None:
    """
    Generate Python source file versions for different Python versions.
    
    Uses ruff to generate version-specific Python files for documentation
    examples, targeting different Python versions.
    
    Args:
        file_path: Path to the source Python file to generate versions for
    """
    target_versions = ["py39", "py310"]
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
        version_file = file_path.with_name(
            file_path.name.replace(".py", f"_{target_version}.py")
        )
        logging.info(f"Writing to {version_file}")
        version_file.write_text(content_format, encoding="utf-8")


if __name__ == "__main__":
    app()
