from tkinter import Event, Frame, Misc, Toplevel

class Dialog(Toplevel):
    def __init__(self, parent: Misc | None, title: str | None = None) -> None: ...
    def body(self, master: Frame) -> Misc | None: ...
    def buttonbox(self) -> None: ...
    def ok(self, event: Event[Misc] | None = None) -> None: ...
    def cancel(self, event: Event[Misc] | None = None) -> None: ...
    def validate(self) -> bool: ...
    def apply(self) -> None: ...

class SimpleDialog:
    def __init__(
        self,
        master: Misc | None,
        text: str = "",
        buttons: list[str] = [],
        default: int | None = None,
        cancel: int | None = None,
        title: str | None = None,
        class_: str | None = None,
    ) -> None: ...
    def go(self) -> int | None: ...
    def return_event(self, event: Event[Misc]) -> None: ...
    def wm_delete_window(self) -> None: ...
    def done(self, num: int) -> None: ...

def askfloat(
    title: str | None,
    prompt: str,
    *,
    initialvalue: float | None = ...,
    minvalue: float | None = ...,
    maxvalue: float | None = ...,
    parent: Misc | None = ...,
) -> float | None: ...
def askinteger(
    title: str | None,
    prompt: str,
    *,
    initialvalue: int | None = ...,
    minvalue: int | None = ...,
    maxvalue: int | None = ...,
    parent: Misc | None = ...,
) -> int | None: ...
def askstring(
    title: str | None,
    prompt: str,
    *,
    initialvalue: str | None = ...,
    show: str | None = ...,
    # minvalue/maxvalue is accepted but not useful.
    parent: Misc | None = ...,
) -> str | None: ...
