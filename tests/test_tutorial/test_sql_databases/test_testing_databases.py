from pathlib import Path


def test_testing_dbs():
    # Import while creating the client to create the DB after starting the test session
    from sql_databases.sql_app.tests.test_sql_app import test_create_user

    test_db = Path("./test.db")
    app_db = Path("./sql_app.db")
    test_create_user()
    test_db.unlink()
    if app_db.is_file():  # pragma: nocover
        app_db.unlink()
