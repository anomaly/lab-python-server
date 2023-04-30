from fastapi import status

from labs.schema.ext import EchoResponse

def test_echo(test_client):
    
    response = test_client.get("/ext/echo")
    parsed_response = EchoResponse.parse_obj(response.json())
    
    expected_response = EchoResponse(
        message="Hello World"
    )

    assert response.status_code == status.HTTP_200_OK
    assert parsed_response == expected_response
