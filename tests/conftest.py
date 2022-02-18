import pytest


@pytest.fixture
def asanabase():
    apikey = "AsanaAPIKey"
    projiect_id = 1234567890123456
    workspace_id = 2345678901234567

    yield apikey, projiect_id, workspace_id