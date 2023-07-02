__all__ = ["GetoptError", "error", "getopt", "gnu_getopt"]

def getopt(
    args: list[str], shortopts: str, longopts: list[str] = []
) -> tuple[list[tuple[str, str]], list[str]]: ...
def gnu_getopt(
    args: list[str], shortopts: str, longopts: list[str] = []
) -> tuple[list[tuple[str, str]], list[str]]: ...

class GetoptError(Exception):
    msg: str
    opt: str
    def __init__(self, msg: str, opt: str = "") -> None: ...

error = GetoptError
