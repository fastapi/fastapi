from __future__ import annotations


def trigger_to_target(s: str) -> str:
    assert s[0] == "<"
    # Strip off the angle brackets
    s = s[1:-1]
    # If there is a [wildcard] or similar, strip that off too
    if s[-1] == "]":
        s = s.split("[")[0]
    return s
