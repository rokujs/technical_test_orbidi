import pytest

def test_create_category(client):
    payload = {
        "name": "restaurantes",
        "description": "Lugares para comer"
    }
    response = client.post("/category/", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Restaurantes"
    assert data["description"] == "Lugares para comer"

def test_create_duplicate_category(client):
    payload = {
        "name": "cafeterias",
        "description": "Lugares para café"
    }
    # First creation
    client.post("/category/", json=payload)

    # Duplicate attempt
    response2 = client.post("/category/", json=payload)

    assert response2.status_code == 400
    assert response2.json()["detail"] == "Category already exists"


def test_list_categories(client):
    # Create two categories
    client.post("/category/", json={"name": "bares", "description": "Lugares para beber"})
    client.post("/category/", json={"name": "parques", "description": "Áreas verdes"})

    response = client.get("/category/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert any(cat["name"] == "Bares" for cat in data)
    assert any(cat["name"] == "Parques" for cat in data)

def test_create_category_missing_name(client):
    payload = {
        "description": "Missing name field"
    }

    response = client.post("/category/", json=payload)
    
    assert response.status_code == 422
    assert "name" in response.text

def test_create_category_strip_and_capitalize(client):
    payload = {
        "name": "   museos   ",
        "description": "Museos de arte"
    }

    response = client.post("/category/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Museos"
