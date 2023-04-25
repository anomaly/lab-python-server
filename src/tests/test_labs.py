import pytest

from labs import __version__


def test_ping(test_client):
    assert test_client != None
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the labs.api API", 
        "root_path": "/api"
    }

def test_version():
    assert __version__ == '0.1.0'
