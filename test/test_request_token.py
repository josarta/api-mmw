import requests
from fastapi import status
from config.db import BASE_URL


def test_login_for_access_token():
    response = requests.post(
        f"{BASE_URL}/api/v1/token",
        json={"username": "dog", "password": "dogpassword"},
    )
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"


def test_read_users_me():
    response = requests.post(
        f"{BASE_URL}/api/v1/token",
        json={"username": "dog", "password": "dogpassword"},
    )
    json_response = response.json()
    access_token = json_response["access_token"]

    response = requests.post(
        f"{BASE_URL}/api/v1/token/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response["username"] == "dog"


def test_incorrect_login():
    response = requests.post(
        f"{BASE_URL}/api/v1/token",
        json={"username": "dog", "password": "dogpassword"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_inactive_user():
    response = requests.post(
        f"{BASE_URL}/api/v1/token",
        json={"username": "dog", "password": "dogpassword"},
    )
    json_response = response.json()
    access_token = json_response["access_token"]

    response = requests.post(
        f"{BASE_URL}/api/v1/token/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Inactive user"}
