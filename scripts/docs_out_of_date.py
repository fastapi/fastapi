from pathlib import Path
from typing import Optional

import git
import typer

app = typer.Typer()

dir_path = Path(__file__).absolute().parent.parent
repo = git.Repo(dir_path)

original_docs = Path("docs/en/docs")


def lang_callback(lang: Optional[str]):
    if lang is None:
        return
    if not lang.isalpha() or len(lang) != 2:
        typer.echo("Use a 2 letter language code, like: es")
        raise typer.Abort()
    lang = lang.lower()
    return lang


@app.command()
def search(lang: str = typer.Argument(..., callback=lang_callback)):
    """
    Search out of date translations for the language LANG.

    LANG should be a 2-letter language code, like: en, es, de, pt, etc.
    """
    target_docs = Path("docs") / lang / "docs"

    orig_prefix_length = len(str(original_docs.absolute())) + 1
    up_to_dates = []
    out_of_dates = []
    for original_doc in original_docs.glob("**/*.md"):
        relative_path = str(original_doc.absolute())[orig_prefix_length:]
        target_doc = target_docs / relative_path
        if not target_doc.exists():
            continue
        orig_committed_date = list(repo.iter_commits(paths=original_doc, max_count=1))[
            0
        ].committed_datetime
        target_committed_date = list(repo.iter_commits(paths=target_doc, max_count=1))[
            0
        ].committed_datetime

        if orig_committed_date > target_committed_date:
            out_of_dates.append(relative_path)
        else:
            up_to_dates.append(relative_path)
    if up_to_dates:
        typer.echo("The followings are up-to-date:")
        typer.secho("\n".join(up_to_dates), fg=typer.colors.GREEN)
        typer.echo("\n")
    if out_of_dates:
        typer.echo("The followings are out-of-date:")
        typer.secho("\n".join(up_to_dates), fg=typer.colors.RED)


if __name__ == "__main__":
    app()
