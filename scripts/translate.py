from functools import lru_cache
from pathlib import Path
from typing import Iterable

import typer
import yaml
from pydantic_ai import Agent

non_translated_sections = (
    "reference/",
    "release-notes.md",
    "fastapi-people.md",
    "external-links.md",
    "newsletter.md",
    "management-tasks.md",
    "management.md",
    "contributing.md",
)


general_prompt = """
For technical terms in English that don't have a common translation term use the original term in English.

For code snippets or fragments, surrounded by backticks (`), don't translate the content, keep the original in English. For example, `list`, `dict`, keep them as is.

The content is written in markdown, write the translation in markdown as well. Don't add triple backticks (`) around the generated translation content.

When there's an example of code, the console or a terminal, normally surrounded by triple backticks and a keyword like "console" or "bash" (e.g. ```console), do not translate the content, keep the original in English.

The original content will be surrounded by triple percentage signs (%) and you should translate it to the target language. Do not include the triple percentage signs in the translation.
"""


@lru_cache
def get_langs() -> dict[str, str]:
    return yaml.safe_load(Path("docs/language_names.yml").read_text())


def generate_lang_path(*, lang: str, path: Path) -> Path:
    en_docs_path = Path("docs/en/docs")
    assert str(path).startswith(str(en_docs_path)), (
        f"Path must be inside {en_docs_path}"
    )
    lang_docs_path = Path(f"docs/{lang}/docs")
    out_path = Path(str(path).replace(str(en_docs_path), str(lang_docs_path)))
    return out_path


def translate_page(*, lang: str, path: Path) -> None:
    langs = get_langs()
    language = langs[lang]
    lang_path = Path(f"docs/{lang}")
    lang_path.mkdir(exist_ok=True)
    lang_prompt_path = lang_path / "llm-prompt.md"
    assert lang_prompt_path.exists(), f"Prompt file not found: {lang_prompt_path}"
    lang_prompt_content = lang_prompt_path.read_text()

    en_docs_path = Path("docs/en/docs")
    assert str(path).startswith(str(en_docs_path)), (
        f"Path must be inside {en_docs_path}"
    )
    out_path = generate_lang_path(lang=lang, path=path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    original_content = path.read_text()
    old_translation: str | None = None
    if out_path.exists():
        old_translation = out_path.read_text()
    agent = Agent("openai:gpt-4o")

    prompt_segments = [
        lang_prompt_content,
        general_prompt,
    ]
    if old_translation:
        prompt_segments.extend(
            [
                "There's an existing previous translation for this content that is probably outdated with old content or old instructions.",
                "Update the translation given your current instructions and the original content.",
                "If you have instructions to translate specific terms or phrases in a specific way, please follow those instructions instead of keeping the old and outdated content.",
                "Previous translation:",
                f"%%%\n{old_translation}%%%",
            ]
        )
    prompt_segments.extend(
        [
            f"Translate to {language} ({lang}).",
            "Original content:",
            f"%%%\n{original_content}%%%",
        ]
    )
    prompt = "\n\n".join(prompt_segments)

    result = agent.run_sync(prompt)
    out_content = f"{result.data.strip()}\n"
    out_path.write_text(out_content)


def iter_paths_to_translate() -> Iterable[Path]:
    """
    Iterate on the markdown files to translate in order of priority.
    """
    first_dirs = [
        Path("docs/en/docs/learn"),
        Path("docs/en/docs/tutorial"),
        Path("docs/en/docs/advanced"),
        Path("docs/en/docs/about"),
        Path("docs/en/docs/how-to"),
    ]
    first_parent = Path("docs/en/docs")
    yield from first_parent.glob("*.md")
    for dir_path in first_dirs:
        yield from dir_path.rglob("*.md")
    first_dirs_str = tuple(str(d) for d in first_dirs)
    for path in Path("docs/en/docs").rglob("*.md"):
        if str(path).startswith(first_dirs_str):
            continue
        if path.parent == first_parent:
            continue
        yield path


def translate_all(lang: str) -> None:
    paths_to_process: list[Path] = []
    for path in iter_paths_to_translate():
        if str(path).replace("docs/en/docs/", "").startswith(non_translated_sections):
            continue
        paths_to_process.append(path)
    print("Original paths:")
    for p in paths_to_process:
        print(f"  - {p}")
    print(f"Total original paths: {len(paths_to_process)}")
    missing_paths: list[Path] = []
    skipped_paths: list[Path] = []
    for p in paths_to_process:
        lang_path = generate_lang_path(lang=lang, path=p)
        if lang_path.exists():
            skipped_paths.append(p)
            continue
        missing_paths.append(p)
    print("Paths to skip:")
    for p in skipped_paths:
        print(f"  - {p}")
    print(f"Total paths to skip: {len(skipped_paths)}")
    print("Paths to process:")
    for p in missing_paths:
        print(f"  - {p}")
    print(f"Total paths to process: {len(missing_paths)}")
    for p in missing_paths:
        print(f"Translating: {p}")
        translate_page(lang="es", path=p)
        print(f"Done translating: {p}")


def main(*, lang: str, path: Path = None) -> None:
    if path:
        translate_page(lang=lang, path=path)
    else:
        translate_all(lang=lang)


if __name__ == "__main__":
    typer.run(main)
