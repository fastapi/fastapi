import json as _json
import typing as _t


class _CompactJSON:
    """Wrapper around json module that strips whitespace."""

    @staticmethod
    def loads(payload: _t.Union[str, bytes]) -> _t.Any:
        return _json.loads(payload)

    @staticmethod
    def dumps(obj: _t.Any, **kwargs: _t.Any) -> str:
        kwargs.setdefault("ensure_ascii", False)
        kwargs.setdefault("separators", (",", ":"))
        return _json.dumps(obj, **kwargs)
