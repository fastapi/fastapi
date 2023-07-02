import pytest

from .._events import (
    ConnectionClosed,
    Data,
    EndOfMessage,
    InformationalResponse,
    Request,
    Response,
)
from .._state import (
    _SWITCH_CONNECT,
    _SWITCH_UPGRADE,
    CLIENT,
    CLOSED,
    DONE,
    IDLE,
    MIGHT_SWITCH_PROTOCOL,
    MUST_CLOSE,
    SEND_BODY,
    SEND_RESPONSE,
    SERVER,
    SWITCHED_PROTOCOL,
    ConnectionState,
)
from .._util import LocalProtocolError


def test_ConnectionState() -> None:
    cs = ConnectionState()

    # Basic event-triggered transitions

    assert cs.states == {CLIENT: IDLE, SERVER: IDLE}

    cs.process_event(CLIENT, Request)
    # The SERVER-Request special case:
    assert cs.states == {CLIENT: SEND_BODY, SERVER: SEND_RESPONSE}

    # Illegal transitions raise an error and nothing happens
    with pytest.raises(LocalProtocolError):
        cs.process_event(CLIENT, Request)
    assert cs.states == {CLIENT: SEND_BODY, SERVER: SEND_RESPONSE}

    cs.process_event(SERVER, InformationalResponse)
    assert cs.states == {CLIENT: SEND_BODY, SERVER: SEND_RESPONSE}

    cs.process_event(SERVER, Response)
    assert cs.states == {CLIENT: SEND_BODY, SERVER: SEND_BODY}

    cs.process_event(CLIENT, EndOfMessage)
    cs.process_event(SERVER, EndOfMessage)
    assert cs.states == {CLIENT: DONE, SERVER: DONE}

    # State-triggered transition

    cs.process_event(SERVER, ConnectionClosed)
    assert cs.states == {CLIENT: MUST_CLOSE, SERVER: CLOSED}


def test_ConnectionState_keep_alive() -> None:
    # keep_alive = False
    cs = ConnectionState()
    cs.process_event(CLIENT, Request)
    cs.process_keep_alive_disabled()
    cs.process_event(CLIENT, EndOfMessage)
    assert cs.states == {CLIENT: MUST_CLOSE, SERVER: SEND_RESPONSE}

    cs.process_event(SERVER, Response)
    cs.process_event(SERVER, EndOfMessage)
    assert cs.states == {CLIENT: MUST_CLOSE, SERVER: MUST_CLOSE}


def test_ConnectionState_keep_alive_in_DONE() -> None:
    # Check that if keep_alive is disabled when the CLIENT is already in DONE,
    # then this is sufficient to immediately trigger the DONE -> MUST_CLOSE
    # transition
    cs = ConnectionState()
    cs.process_event(CLIENT, Request)
    cs.process_event(CLIENT, EndOfMessage)
    assert cs.states[CLIENT] is DONE
    cs.process_keep_alive_disabled()
    assert cs.states[CLIENT] is MUST_CLOSE


def test_ConnectionState_switch_denied() -> None:
    for switch_type in (_SWITCH_CONNECT, _SWITCH_UPGRADE):
        for deny_early in (True, False):
            cs = ConnectionState()
            cs.process_client_switch_proposal(switch_type)
            cs.process_event(CLIENT, Request)
            cs.process_event(CLIENT, Data)
            assert cs.states == {CLIENT: SEND_BODY, SERVER: SEND_RESPONSE}

            assert switch_type in cs.pending_switch_proposals

            if deny_early:
                # before client reaches DONE
                cs.process_event(SERVER, Response)
                assert not cs.pending_switch_proposals

            cs.process_event(CLIENT, EndOfMessage)

            if deny_early:
                assert cs.states == {CLIENT: DONE, SERVER: SEND_BODY}
            else:
                assert cs.states == {
                    CLIENT: MIGHT_SWITCH_PROTOCOL,
                    SERVER: SEND_RESPONSE,
                }

                cs.process_event(SERVER, InformationalResponse)
                assert cs.states == {
                    CLIENT: MIGHT_SWITCH_PROTOCOL,
                    SERVER: SEND_RESPONSE,
                }

                cs.process_event(SERVER, Response)
                assert cs.states == {CLIENT: DONE, SERVER: SEND_BODY}
                assert not cs.pending_switch_proposals


_response_type_for_switch = {
    _SWITCH_UPGRADE: InformationalResponse,
    _SWITCH_CONNECT: Response,
    None: Response,
}


def test_ConnectionState_protocol_switch_accepted() -> None:
    for switch_event in [_SWITCH_UPGRADE, _SWITCH_CONNECT]:
        cs = ConnectionState()
        cs.process_client_switch_proposal(switch_event)
        cs.process_event(CLIENT, Request)
        cs.process_event(CLIENT, Data)
        assert cs.states == {CLIENT: SEND_BODY, SERVER: SEND_RESPONSE}

        cs.process_event(CLIENT, EndOfMessage)
        assert cs.states == {CLIENT: MIGHT_SWITCH_PROTOCOL, SERVER: SEND_RESPONSE}

        cs.process_event(SERVER, InformationalResponse)
        assert cs.states == {CLIENT: MIGHT_SWITCH_PROTOCOL, SERVER: SEND_RESPONSE}

        cs.process_event(SERVER, _response_type_for_switch[switch_event], switch_event)
        assert cs.states == {CLIENT: SWITCHED_PROTOCOL, SERVER: SWITCHED_PROTOCOL}


def test_ConnectionState_double_protocol_switch() -> None:
    # CONNECT + Upgrade is legal! Very silly, but legal. So we support
    # it. Because sometimes doing the silly thing is easier than not.
    for server_switch in [None, _SWITCH_UPGRADE, _SWITCH_CONNECT]:
        cs = ConnectionState()
        cs.process_client_switch_proposal(_SWITCH_UPGRADE)
        cs.process_client_switch_proposal(_SWITCH_CONNECT)
        cs.process_event(CLIENT, Request)
        cs.process_event(CLIENT, EndOfMessage)
        assert cs.states == {CLIENT: MIGHT_SWITCH_PROTOCOL, SERVER: SEND_RESPONSE}
        cs.process_event(
            SERVER, _response_type_for_switch[server_switch], server_switch
        )
        if server_switch is None:
            assert cs.states == {CLIENT: DONE, SERVER: SEND_BODY}
        else:
            assert cs.states == {CLIENT: SWITCHED_PROTOCOL, SERVER: SWITCHED_PROTOCOL}


def test_ConnectionState_inconsistent_protocol_switch() -> None:
    for client_switches, server_switch in [
        ([], _SWITCH_CONNECT),
        ([], _SWITCH_UPGRADE),
        ([_SWITCH_UPGRADE], _SWITCH_CONNECT),
        ([_SWITCH_CONNECT], _SWITCH_UPGRADE),
    ]:
        cs = ConnectionState()
        for client_switch in client_switches:  # type: ignore[attr-defined]
            cs.process_client_switch_proposal(client_switch)
        cs.process_event(CLIENT, Request)
        with pytest.raises(LocalProtocolError):
            cs.process_event(SERVER, Response, server_switch)


def test_ConnectionState_keepalive_protocol_switch_interaction() -> None:
    # keep_alive=False + pending_switch_proposals
    cs = ConnectionState()
    cs.process_client_switch_proposal(_SWITCH_UPGRADE)
    cs.process_event(CLIENT, Request)
    cs.process_keep_alive_disabled()
    cs.process_event(CLIENT, Data)
    assert cs.states == {CLIENT: SEND_BODY, SERVER: SEND_RESPONSE}

    # the protocol switch "wins"
    cs.process_event(CLIENT, EndOfMessage)
    assert cs.states == {CLIENT: MIGHT_SWITCH_PROTOCOL, SERVER: SEND_RESPONSE}

    # but when the server denies the request, keep_alive comes back into play
    cs.process_event(SERVER, Response)
    assert cs.states == {CLIENT: MUST_CLOSE, SERVER: SEND_BODY}


def test_ConnectionState_reuse() -> None:
    cs = ConnectionState()

    with pytest.raises(LocalProtocolError):
        cs.start_next_cycle()

    cs.process_event(CLIENT, Request)
    cs.process_event(CLIENT, EndOfMessage)

    with pytest.raises(LocalProtocolError):
        cs.start_next_cycle()

    cs.process_event(SERVER, Response)
    cs.process_event(SERVER, EndOfMessage)

    cs.start_next_cycle()
    assert cs.states == {CLIENT: IDLE, SERVER: IDLE}

    # No keepalive

    cs.process_event(CLIENT, Request)
    cs.process_keep_alive_disabled()
    cs.process_event(CLIENT, EndOfMessage)
    cs.process_event(SERVER, Response)
    cs.process_event(SERVER, EndOfMessage)

    with pytest.raises(LocalProtocolError):
        cs.start_next_cycle()

    # One side closed

    cs = ConnectionState()
    cs.process_event(CLIENT, Request)
    cs.process_event(CLIENT, EndOfMessage)
    cs.process_event(CLIENT, ConnectionClosed)
    cs.process_event(SERVER, Response)
    cs.process_event(SERVER, EndOfMessage)

    with pytest.raises(LocalProtocolError):
        cs.start_next_cycle()

    # Succesful protocol switch

    cs = ConnectionState()
    cs.process_client_switch_proposal(_SWITCH_UPGRADE)
    cs.process_event(CLIENT, Request)
    cs.process_event(CLIENT, EndOfMessage)
    cs.process_event(SERVER, InformationalResponse, _SWITCH_UPGRADE)

    with pytest.raises(LocalProtocolError):
        cs.start_next_cycle()

    # Failed protocol switch

    cs = ConnectionState()
    cs.process_client_switch_proposal(_SWITCH_UPGRADE)
    cs.process_event(CLIENT, Request)
    cs.process_event(CLIENT, EndOfMessage)
    cs.process_event(SERVER, Response)
    cs.process_event(SERVER, EndOfMessage)

    cs.start_next_cycle()
    assert cs.states == {CLIENT: IDLE, SERVER: IDLE}


def test_server_request_is_illegal() -> None:
    # There used to be a bug in how we handled the Request special case that
    # made this allowed...
    cs = ConnectionState()
    with pytest.raises(LocalProtocolError):
        cs.process_event(SERVER, Request)
