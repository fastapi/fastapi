# Starlette currently accesses this deprecated alias when importing its test client.
# https://github.com/Kludex/starlette/issues/3497
def pytest_configure(config):
    config.addinivalue_line(
        "filterwarnings",
        "ignore:The anyio.abc.BlockingPortal alias is deprecated:DeprecationWarning:starlette.testclient",
    )
