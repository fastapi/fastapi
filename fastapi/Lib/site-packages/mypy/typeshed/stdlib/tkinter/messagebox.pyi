import sys
from tkinter.commondialog import Dialog
from typing import ClassVar

if sys.version_info >= (3, 9):
    __all__ = [
        "showinfo",
        "showwarning",
        "showerror",
        "askquestion",
        "askokcancel",
        "askyesno",
        "askyesnocancel",
        "askretrycancel",
    ]

ERROR: str
INFO: str
QUESTION: str
WARNING: str
ABORTRETRYIGNORE: str
OK: str
OKCANCEL: str
RETRYCANCEL: str
YESNO: str
YESNOCANCEL: str
ABORT: str
RETRY: str
IGNORE: str
CANCEL: str
YES: str
NO: str

class Message(Dialog):
    command: ClassVar[str]

def showinfo(
    title: str | None = None, message: str | None = None, **options
) -> str: ...
def showwarning(
    title: str | None = None, message: str | None = None, **options
) -> str: ...
def showerror(
    title: str | None = None, message: str | None = None, **options
) -> str: ...
def askquestion(
    title: str | None = None, message: str | None = None, **options
) -> str: ...
def askokcancel(
    title: str | None = None, message: str | None = None, **options
) -> bool: ...
def askyesno(
    title: str | None = None, message: str | None = None, **options
) -> bool: ...
def askyesnocancel(
    title: str | None = None, message: str | None = None, **options
) -> bool | None: ...
def askretrycancel(
    title: str | None = None, message: str | None = None, **options
) -> bool: ...
