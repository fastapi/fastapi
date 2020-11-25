import importlib
from pathlib import Path


def test_testing_dbs():
    test_db = Path("./test.db")
    if test_db.is_file():  # pragma: nocover
        test_db.unlink()
    # Import while creating the client to create the DB after starting the test session
    from docs_src.sql_databases.sql_app.tests import test_sql_app

    # Ensure import side effects are re-executed
    importlib.reload(test_sql_app)
    test_sql_app.test_create_user()
    if test_db.is_file():  # pragma: nocover
        test_db.unlink()
