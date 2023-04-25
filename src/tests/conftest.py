"""

"""
import pytest

@pytest.fixture(scope="module")
def test_client():
    from fastapi.testclient import TestClient
    from labs.api import app
    return TestClient(app)
