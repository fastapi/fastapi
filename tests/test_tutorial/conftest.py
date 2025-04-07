import pytest


@pytest.fixture(autouse=True)
def deactivate_blockbuster(blockbuster):
    blockbuster.deactivate()
