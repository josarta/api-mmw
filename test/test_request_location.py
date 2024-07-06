import requests
from fastapi import status 

BASE_URL = 'http://127.0.0.1:8000/'  


def test_create_location_bad():
    response = requests.post(f'{BASE_URL}/locations', json={"latitude": 40.712776, "longitude": -74.005974})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_location_ok():
    response = requests.post(f'{BASE_URL}/locations', 
    json={
         "location_id": 0,
         "latitude": 40.712776,
         "longitude": -74.005974,
         "created_at": "2024-07-05T20:55:51.240Z"
    })
    assert response.status_code == status.HTTP_200_OK
    assert 'location_id' in response.json()


def test_get_all_locations():
    response = requests.get(f'{BASE_URL}/locations')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_location_by_id():
    location_id = 1  
    response = requests.get(f'{BASE_URL}/locations/{location_id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['location_id'] == location_id


def test_update_location():
    location_id = 1 
    response = requests.put(f'{BASE_URL}/locations/{location_id}', 
    json={
         "location_id": 0,
         "latitude": 34.052235,
         "longitude": -118.243683,
         "created_at": "2024-07-05T20:55:51.240Z"
    })
    assert response.status_code == status.HTTP_200_OK
    updated_location = response.json()
    assert updated_location['latitude'] == 34.052235
    assert updated_location['longitude'] == -118.243683


def test_delete_location():
    location_id = 31 
    response = requests.delete(f'{BASE_URL}/locations/{location_id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT

