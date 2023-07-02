from typing import List, Type, Union, ValuesView, cast

from .._connection import NEED_DATA, PAUSED, Connection
from .._events import (
    ConnectionClosed,
    Data,
    Event,
)
from .._state import CLIENT, SERVER
from .._util import Sentinel

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore


def get_all_events(conn: Connection) -> List[Event]:
    got_events = []
    while True:
        event = conn.next_event()
        if event in (NEED_DATA, PAUSED):
            break
        event = cast(Event, event)
        got_events.append(event)
        if type(event) is ConnectionClosed:
            break
    return got_events


def receive_and_get(conn: Connection, data: bytes) -> List[Event]:
    conn.receive_data(data)
    return get_all_events(conn)


# Merges adjacent Data events, converts payloads to bytestrings, and removes
# chunk boundaries.
def normalize_data_events(in_events: List[Event]) -> List[Event]:
    out_events: List[Event] = []
    for event in in_events:
        if type(event) is Data:
            event = Data(data=bytes(event.data), chunk_start=False, chunk_end=False)
        if out_events and type(out_events[-1]) is type(event) is Data:
            out_events[-1] = Data(
                data=out_events[-1].data + event.data,
                chunk_start=out_events[-1].chunk_start,
                chunk_end=out_events[-1].chunk_end,
            )
        else:
            out_events.append(event)
    return out_events


# Given that we want to write tests that push some events through a Connection
# and check that its state updates appropriately... we might as make a habit
# of pushing them through two Connections with a fake network link in
# between.
class ConnectionPair:
    def __init__(self) -> None:
        self.conn = {CLIENT: Connection(CLIENT), SERVER: Connection(SERVER)}
        self.other = {CLIENT: SERVER, SERVER: CLIENT}

    @property
    def conns(self) -> ValuesView[Connection]:
        return self.conn.values()

    # expect="match" if expect=send_events; expect=[...] to say what expected
    def send(
        self,
        role: Type[Sentinel],
        send_events: Union[List[Event], Event],
        expect: Union[List[Event], Event, Literal["match"]] = "match",
    ) -> bytes:
        if not isinstance(send_events, list):
            send_events = [send_events]
        data = b""
        closed = False
        for send_event in send_events:
            new_data = self.conn[role].send(send_event)
            if new_data is None:
                closed = True
            else:
                data += new_data
        # send uses b"" to mean b"", and None to mean closed
        # receive uses b"" to mean closed, and None to mean "try again"
        # so we have to translate between the two conventions
        if data:
            self.conn[self.other[role]].receive_data(data)
        if closed:
            self.conn[self.other[role]].receive_data(b"")
        got_events = get_all_events(self.conn[self.other[role]])
        if expect == "match":
            expect = send_events
        if not isinstance(expect, list):
            expect = [expect]
        assert got_events == expect
        return data
