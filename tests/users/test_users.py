def test_create_user(client):
    response = client.post("/api/v1/users/", json={
        "name": "Sahir Bhat",
        "email": "sahir@test.com",
        "password": "Test@1234",
        "role": "developer",
        "phone": "1234567890"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "sahir@test.com"

def test_create_user_duplicate(client):
    # first create
    client.post("/api/v1/users/", json={
        "name": "Sahir Bhat",
        "email": "sahir@test.com",
        "password": "Test@1234",
        "role": "developer",
        "phone": "1234567890"
    })
    # duplicate
    response = client.post("/api/v1/users/", json={
        "name": "Sahir Bhat",
        "email": "sahir@test.com",
        "password": "Test@1234",
        "role": "developer",
        "phone": "1234567890"
    })
    assert response.status_code == 400