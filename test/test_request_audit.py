import requests
from fastapi import status 
from config.db import BASE_URL


def test_get_all_audits():
    response = requests.get(f'{BASE_URL}/audit')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_delete_category():
    count_audits = 20 
    response = requests.get(f'{BASE_URL}/audit/count')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['total'] == count_audits


