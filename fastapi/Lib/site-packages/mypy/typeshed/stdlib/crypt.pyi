import sys

if sys.platform != "win32":
    class _Method: ...
    METHOD_CRYPT: _Method
    METHOD_MD5: _Method
    METHOD_SHA256: _Method
    METHOD_SHA512: _Method
    METHOD_BLOWFISH: _Method
    methods: list[_Method]
    def mksalt(method: _Method | None = None, *, rounds: int | None = None) -> str: ...
    def crypt(word: str, salt: str | _Method | None = None) -> str: ...
