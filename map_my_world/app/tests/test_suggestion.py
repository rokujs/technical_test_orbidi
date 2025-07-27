import pytest
from app.models.review import Review
from core.models.user import User


def test_list_suggestions_empty(client):
    # Query with no data in DB
    params = {
        "latitude": 40.0,
        "longitude": -73.0,
        "category_id": 1,
        "page": 0,
        "limit": 5,
    }

    response = client.get("/suggestions/", params=params)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 0


def test_list_suggestions_with_data(client):
    # Create category
    cat_payload = {"name": "parks", "description": "Green areas"}
    cat_resp = client.post("/category/", json=cat_payload)
    category_id = cat_resp.json()["id"]

    # Create location
    loc_payload = {
        "name": "central park",
        "description": "NYC park",
        "latitude": 40.785091,
        "longitude": -73.968285,
    }
    client.post("/location/", json=loc_payload)

    # Query suggestions
    params = {
        "latitude": 40.785091,
        "longitude": -73.968285,
        "category_id": category_id,
        "page": 0,
        "limit": 5,
    }
    response = client.get("/suggestions/", params=params)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    suggestion = data[0]

    assert "location" in suggestion
    assert "category" in suggestion
    assert "reviews" in suggestion


def test_suggestions_missing_latitude(client):
    params = {"longitude": -73.0, "category_id": 1, "page": 0, "limit": 5}

    response = client.get("/suggestions/", params=params)

    assert response.status_code == 422
    assert "latitude" in response.text


def test_suggestions_out_of_range(client):
    # Create category and location far from query point
    cat_payload = {"name": "mountains", "description": "High places"}
    cat_resp = client.post("/category/", json=cat_payload)
    category_id = cat_resp.json()["id"]

    loc_payload = {
        "name": "everest",
        "description": "Highest mountain",
        "latitude": 27.9881,
        "longitude": 86.9250,
    }
    client.post("/location/", json=loc_payload)

    # Query with a distant location
    params = {
        "latitude": 40.785091,
        "longitude": -73.968285,
        "category_id": category_id,
        "page": 0,
        "limit": 5,
    }
    response = client.get("/suggestions/", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_suggestions_with_reviews(client, db_session):
    # Create category
    cat_payload = {"name": "cafes", "description": "Coffee places"}
    cat_resp = client.post("/category/", json=cat_payload)
    category_id = cat_resp.json()["id"]

    # Create location
    loc_payload = {
        "name": "starbucks",
        "description": "Coffee shop",
        "latitude": 40.785091,
        "longitude": -73.968285,
    }
    loc_resp = client.post("/location/", json=loc_payload)
    location_id = loc_resp.json()["id"]

    # Create user
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="fakehashedpassword",
    )
    db_session.add(user)
    db_session.commit()

    # Insert review directly into the database
    review = Review(
        location_id=location_id,
        category_id=category_id,
        user_id=user.id,
        rating=5,
        review="Great coffee!",
    )
    db_session.add(review)
    db_session.commit()

    # Query suggestions
    params = {
        "latitude": 40.785333,
        "longitude": -73.968285,
        "category_id": category_id,
        "page": 0,
        "limit": 5,
    }
    response = client.get("/suggestions/", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    suggestion = data[0]
    assert "reviews" in suggestion
    assert isinstance(suggestion["reviews"], list)
    assert any(r["review"] == "Great coffee!" for r in suggestion["reviews"])
