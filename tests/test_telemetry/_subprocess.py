import json
import os
import subprocess
import sys
from functools import wraps
from importlib import import_module
from inspect import unwrap


def run_in_subprocess(function):
    """Run a test in a fresh interpreter to isolate SDK globals and monkeypatches."""

    @wraps(function)
    def wrapper(**kwargs):
        env = {
            name: value
            for name, value in os.environ.items()
            if not name.startswith(("OTEL_", "LOGFIRE_", "SENTRY_"))
        }
        env["PYDANTIC_DISABLE_PLUGINS"] = "__all__"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "tests.test_telemetry._subprocess",
                function.__module__,
                function.__name__,
                json.dumps(kwargs),
            ],
            env=env,
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0, result.stdout + result.stderr

    return wrapper


if __name__ == "__main__":
    module_name, function_name, arguments = sys.argv[1:]
    function = getattr(import_module(module_name), function_name)
    unwrap(function)(**json.loads(arguments))
