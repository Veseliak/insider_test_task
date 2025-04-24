import time

import pytest
import requests
import random

BASE_URL = "https://petstore.swagger.io/v2"
HEADERS = {"Content-Type": "application/json"}

# Utility to generate a unique pet ID
def generate_pet_id():
    return random.randint(100000, 999999)

# Default payload structure
def pet_payload(pet_id, name="Doggo", status="available"):
    return {
        "id": pet_id,
        "name": name,
        "photoUrls": ["https://example.com/photo.jpg"],
        "status": status
    }

@pytest.fixture(scope="module")
def pet_id():
    return generate_pet_id()

@pytest.fixture(scope="module")
def created_pet(pet_id):
    payload = pet_payload(pet_id)
    response = requests.post(f"{BASE_URL}/pet", json=payload, headers=HEADERS)
    print("Create PET:", response.status_code, response.text)  # Додай це
    assert response.status_code == 200
    return pet_id

def wait_for_pet_to_exist(pet_id, retries=5, delay=1):
    for _ in range(retries):
        response = requests.get(f"{BASE_URL}/pet/{pet_id}")
        if response.status_code == 200:
            return response
        time.sleep(delay)
    return response  # останній результат

# CREATE tests
def test_create_pet_positive(pet_id):
    payload = pet_payload(pet_id)
    response = requests.post(f"{BASE_URL}/pet", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pet_id
    assert data["name"] == "Doggo"

def test_create_pet_negative_missing_fields():
    payload = {"id": generate_pet_id()}  # немає name і status
    response = requests.post(f"{BASE_URL}/pet", json=payload, headers=HEADERS)
    assert response.status_code in (400, 500) or "name" not in response.json()

# READ tests
def test_get_pet_positive(created_pet):
    response = wait_for_pet_to_exist(created_pet)
    assert response.status_code == 200

def test_get_pet_negative():
    response = requests.get(f"{BASE_URL}/pet/0")
    assert response.status_code == 404

# UPDATE tests
def test_update_pet_positive(created_pet):
    updated_payload = pet_payload(created_pet, name="Catto", status="sold")
    response = requests.put(f"{BASE_URL}/pet", json=updated_payload, headers=HEADERS)
    assert response.status_code == 200

def test_update_pet_negative():
    pet_id = generate_pet_id()
    payload = {"id": pet_id, "unknownField": "???"}
    response = requests.put(f"{BASE_URL}/pet", json=payload, headers=HEADERS)
    # Навіть якщо 200, перевір, що name/status не змінилися
    get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
    assert get_response.status_code == 404  # бо такого pet не існує

# DELETE tests
def test_delete_pet_positive(created_pet):
    response = requests.delete(f"{BASE_URL}/pet/{created_pet}")
    assert response.status_code == 200

def test_delete_pet_negative():
    non_existing_id = 0
    response = requests.delete(f"{BASE_URL}/pet/{non_existing_id}")
    assert response.status_code == 404