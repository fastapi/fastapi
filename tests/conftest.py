import pytest
from blockbuster import blockbuster_ctx


@pytest.fixture(autouse=True)
def blockbuster():
    with blockbuster_ctx("fastapi") as bb:
        bb.functions["io.BufferedReader.read"].can_block_in(
            "starlette/testclient.py", "receive"
        )
        for func in [
            "os.stat",
            "io.TextIOWrapper.read",
        ]:
            bb.functions[func].can_block_in(
                "pydantic/networks.py", "import_email_validator"
            )
        yield bb
