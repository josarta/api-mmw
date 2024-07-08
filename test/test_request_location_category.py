import requests
from fastapi import status
from config.db import BASE_URL


def test_get_location_category_reviews():
    response = requests.get(f"{BASE_URL}/api/v1/location-category")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_location_category_reviews_count():
    total = 1
    response = requests.get(f"{BASE_URL}/api/v1/location-category/count")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == total


def test_create_new_location_category_reviews():
    response = requests.post(
        f"{BASE_URL}/api/v1/location-category",
        json={"location_id": 5, "category_id": 6},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "review_id" in response.json()


def test_get_location_category_reviews():
    review_id = 1
    response = requests.get(f"{BASE_URL}/api/v1/location-category/{review_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["review_id"] == review_id


def test_update_location_category():
    review_id = 1
    response = requests.put(
        f"{BASE_URL}/api/v1/location-category/{review_id}",
        json={"location_id": 8, "category_id": 8},
    )
    assert response.status_code == status.HTTP_200_OK
    updated_location_category = response.json()
    assert updated_location_category.category["location_id"] == 8
    assert updated_location_category.location["category_id"] == 8


def test_delete_location():
    review_id = 31
    response = requests.delete(f"{BASE_URL}/api/v1/location-category/{review_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_all_location_consulting_categorys():
    category_id = 8
    response = requests.get(
        f"{BASE_URL}/api/v1/location-category/locations/{category_id}"
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_last_ten_scan_recommender():
    response = requests.get(f"{BASE_URL}/api/v1/location-category/scan/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
