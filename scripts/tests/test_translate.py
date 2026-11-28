import importlib
from pathlib import Path

import pytest

# scripts/ is a namespace package (no __init__.py), so a static
# "from scripts import translate" makes mypy register scripts/translate.py under
# two module names ("translate" and "scripts.translate") when it is checked
# alongside this file. Importing through the runtime module path keeps a single
# identity for mypy's scoped file list.
translate = importlib.import_module("scripts.translate")


class FakeAgentResult:
    output = "traducción rota\n"


class FakeAgent:
    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def run_sync(self, prompt: str, *args: object, **kwargs: object) -> FakeAgentResult:
        return FakeAgentResult()


def fake_check_translation(*args: object, **kwargs: object) -> list[str]:
    raise ValueError("Translation does not match the original document")


def test_translate_page_does_not_save_rejected_translation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docs" / "es").mkdir(parents=True)
    (tmp_path / "docs" / "es" / "llm-prompt.md").write_text(
        "prompt\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "en" / "docs").mkdir(parents=True)
    (tmp_path / "docs" / "en" / "docs" / "index.md").write_text(
        "# Title\n\nHello\n", encoding="utf-8"
    )

    monkeypatch.setattr(
        translate, "get_langs", lambda: {"en": "English", "es": "Español"}
    )
    monkeypatch.setattr(translate, "Agent", FakeAgent)
    monkeypatch.setattr(translate, "check_translation", fake_check_translation)

    with pytest.raises(RuntimeError, match="Translation failed"):
        translate.translate_page(language="es", en_path=Path("docs/en/docs/index.md"))

    assert not (tmp_path / "docs" / "es" / "docs" / "index.md").exists()
