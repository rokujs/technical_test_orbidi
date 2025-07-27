import pytest

def test_create_location(client):
    payload = {
        "name": "central park",
        "description": "A large public park in NYC",
        "latitude": 40.785091,
        "longitude": -73.968285
    }

    response = client.post("/location/", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Central park"
    assert data["description"] == "A large public park in NYC"
    assert data["latitude"] == 40.785091
    assert data["longitude"] == -73.968285

def test_create_duplicate_location(client):
    payload = {
        "name": "statue of liberty",
        "description": "Famous monument",
        "latitude": 40.689247,
        "longitude": -74.044502
    }

    # First creation
    client.post("/location/", json=payload)
    
    # Duplicate attempt
    response2 = client.post("/location/", json=payload)
    
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Location already exists"

def test_list_locations(client):
    # Create two locations
    client.post("/location/", json={
        "name": "empire state building",
        "description": "Skyscraper in NYC",
        "latitude": 40.748817,
        "longitude": -73.985428
    })
    client.post("/location/", json={
        "name": "brooklyn bridge",
        "description": "Historic bridge",
        "latitude": 40.706086,
        "longitude": -73.996864
    })

    response = client.get("/location/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert any(loc["name"] == "Empire state building" for loc in data)
    assert any(loc["name"] == "Brooklyn bridge" for loc in data)
