from .._events import (
    Data,
    EndOfMessage,
    Response,
)
from .helpers import normalize_data_events


def test_normalize_data_events() -> None:
    assert normalize_data_events(
        [
            Data(data=bytearray(b"1")),
            Data(data=b"2"),
            Response(status_code=200, headers=[]),  # type: ignore[arg-type]
            Data(data=b"3"),
            Data(data=b"4"),
            EndOfMessage(),
            Data(data=b"5"),
            Data(data=b"6"),
            Data(data=b"7"),
        ]
    ) == [
        Data(data=b"12"),
        Response(status_code=200, headers=[]),  # type: ignore[arg-type]
        Data(data=b"34"),
        EndOfMessage(),
        Data(data=b"567"),
    ]
