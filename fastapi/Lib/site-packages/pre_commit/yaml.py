from __future__ import annotations

import functools
from typing import Any

import yaml

Loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
yaml_load = functools.partial(yaml.load, Loader=Loader)
Dumper = getattr(yaml, "CSafeDumper", yaml.SafeDumper)


def yaml_dump(o: Any, **kwargs: Any) -> str:
    # when python/mypy#1484 is solved, this can be `functools.partial`
    return yaml.dump(
        o,
        Dumper=Dumper,
        default_flow_style=False,
        indent=4,
        sort_keys=False,
        **kwargs,
    )
