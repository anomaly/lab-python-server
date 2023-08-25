""" Configuration required for tests to run

Note that fastapi makes available a test client that can be used to
test the API endpoints. This will call the endpoints internally.

For the taskiq to work we have configured it to use the InMemoryBroker
otherwise it will try to connect to a redis server.

Please note you will require pytest-env for the environment variables
to work which are set via pyproject.toml
"""
import pytest


@pytest.fixture(scope='session')
def test_client():
    from fastapi.testclient import TestClient
    from labs.api import app
    return TestClient(app)


@pytest.fixture
def anyio_backend():
    """ Since taskiq is fully async, we suggest using anyio

    See configuration described in the docs:
    https://taskiq-python.github.io/guide/testing-taskiq.html#async-tests
    """
    return 'asyncio'
