import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("optional_module_name", ("ujson", "orjson"))
def test_responses_imports_when_optional_json_import_raises_import_error(
    optional_module_name: str,
) -> None:
    code = textwrap.dedent(
        f"""
        import importlib

        real_import_module = importlib.import_module

        def fake_import_module(name, package=None):
            if name == {optional_module_name!r}:
                raise ImportError("simulated optional dependency load failure")
            return real_import_module(name, package)

        importlib.import_module = fake_import_module

        import fastapi.responses as responses

        assert getattr(responses, {optional_module_name!r}) is None
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        cwd=REPO_ROOT,
        text=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout
