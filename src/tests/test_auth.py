import pytest 

from fastapi import status
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm

from labs.schema.auth import Token, SignupRequest, SignupResponse

@pytest.fixture()
def signup_request(faker):
    return SignupRequest(
        password=faker.password(),
        email=faker.company_email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
    )

def test_signup(test_client, signup_request):

    response = test_client.post(
        "/signup", 
        json=signup_request.dict()
    )

    expected_response = SignupResponse(
        success=True,
        email=signup_request.email
    )

    parsed_body = SignupResponse.parse_obj(response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert parsed_body == expected_response

def test_verify(test_client):
    assert 1 == 1

def test_login(test_client, signup_request):
    assert 1 == 1
