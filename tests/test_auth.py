def test_register_success(client):
    response = client.post("/auth/register", json={
        "nombre": "Juan",
        "email": "juan@test.com",
        "password": "123456",
        "telefono": "123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "juan@test.com"
    assert data["rol"] == "adoptante"

def test_register_duplicate_email(client):
    payload = {
        "nombre": "Juan",
        "email": "juan@test.com",
        "password": "123456"
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email ya registrado"

def test_login_success(client):
    client.post("/auth/register", json={
        "nombre": "Juan",
        "email": "juan@test.com",
        "password": "123456"
    })
    response = client.post("/auth/login", json={
        "email": "juan@test.com",
        "password": "123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post("/auth/login", json={
        "email": "fake@test.com",
        "password": "wrong"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"