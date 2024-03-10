from unittest.mock import MagicMock

from pytest_mock import MockerFixture
from sqlmodel import select

from app.backend_pre_start import init, logger


def test_init_successful_connection(mocker: MockerFixture) -> None:
    engine_mock = MagicMock()

    session_mock = MagicMock()
    exec_mock = MagicMock(return_value=True)
    session_mock.configure_mock(**{"exec.return_value": exec_mock})
    mocker.patch("sqlmodel.Session", return_value=session_mock)

    mocker.patch.object(logger, "info")
    mocker.patch.object(logger, "error")
    mocker.patch.object(logger, "warn")

    try:
        init(engine_mock)
        connection_successful = True
    except Exception:
        connection_successful = False

    assert (
        connection_successful
    ), "The database connection should be successful and not raise an exception."

    assert session_mock.exec.called_once_with(
        select(1)
    ), "The session should execute a select statement once."
