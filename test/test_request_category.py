import requests
from fastapi import status 

BASE_URL = 'http://127.0.0.1:8000/'  


def test_create_category_bad():
    response = requests.post(f'{BASE_URL}/categories', json={"name": 'Cat'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_category_ok():
    response = requests.post(f'{BASE_URL}/categories', 
    json={
         "category_id": 11,
         "name": 'Cat',
         "created_at": "2024-07-05T20:55:51.240Z"
    })
    assert response.status_code == status.HTTP_200_OK
    assert 'category_id' in response.json()


def test_get_all_categories():
    response = requests.get(f'{BASE_URL}/categories')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_category_by_id():
    category_id = 1  
    response = requests.get(f'{BASE_URL}/categories/{category_id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['category_id'] == category_id


def test_update_category():
    category_id = 1 
    response = requests.put(f'{BASE_URL}/categories/{category_id}', 
    json={
         "category_id": 1,
         "name": 'Cat',
         "created_at": "2024-07-05T20:55:51.240Z"
    })
    assert response.status_code == status.HTTP_200_OK
    updated_category = response.json()
    assert updated_category['name'] == 'Cat'
   


def test_delete_category():
    category_id = 12 
    response = requests.delete(f'{BASE_URL}/categories/{category_id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT


