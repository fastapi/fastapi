import asyncio
from contextlib import asynccontextmanager
from unittest.mock import Mock, patch

from docs_src.dependencies.tutorial007_py39 import get_db


def test_get_db():  # Just for coverage
    async def test_async_gen():
        cm = asynccontextmanager(get_db)
        async with cm() as db_session:
            return db_session

    dbsession_moock = Mock()

    with patch(
        "docs_src.dependencies.tutorial007_py39.DBSession",
        return_value=dbsession_moock,
        create=True,
    ):
        value = asyncio.run(test_async_gen())

    assert value is dbsession_moock
    dbsession_moock.close.assert_called_once()
