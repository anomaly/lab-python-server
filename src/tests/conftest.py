"""

"""
import pytest

@pytest.fixture(scope='session')
def test_client():
    from fastapi.testclient import TestClient
    from labs.api import app
    return TestClient(app)
