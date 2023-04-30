from fastapi import status

def test_echo(test_client):
    response = test_client.get("/ext/echo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}
