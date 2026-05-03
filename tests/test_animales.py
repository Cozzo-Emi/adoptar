from app.models.usuario import Usuario, UserRole
from app.services.auth import hash_password, create_access_token
from tests.conftest import TestingSessionLocal


def create_admin_token():
    db = TestingSessionLocal()
    admin = Usuario(
        nombre="Admin",
        email="admin@test.com",
        password_hash=hash_password("123456"),
        rol=UserRole.admin
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    token = create_access_token({"sub": str(admin.id), "rol": admin.rol.value})
    db.close()
    return token


def create_user_token():
    db = TestingSessionLocal()
    user = Usuario(
        nombre="User",
        email="user@test.com",
        password_hash=hash_password("123456"),
        rol=UserRole.adoptante
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id), "rol": user.rol.value})
    db.close()
    return token


def test_list_animals_empty(client):
    response = client.get("/animals/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_animal_admin(client):
    token = create_admin_token()
    response = client.post(
        "/animals/",
        headers={"Authorization": f"Bearer {token}"},
        data={"nombre": "Firulais", "especie": "Perro"}
    )
    assert response.status_code == 201
    assert response.json()["nombre"] == "Firulais"


def test_create_animal_no_auth(client):
    response = client.post("/animals/", data={"nombre": "Firulais", "especie": "Perro"})
    assert response.status_code == 401


def test_create_animal_not_admin(client):
    token = create_user_token()
    response = client.post(
        "/animals/",
        headers={"Authorization": f"Bearer {token}"},
        data={"nombre": "Firulais", "especie": "Perro"}
    )
    assert response.status_code == 403


def test_get_animal_by_id(client):
    token = create_admin_token()
    create = client.post(
        "/animals/",
        headers={"Authorization": f"Bearer {token}"},
        data={"nombre": "Firulais", "especie": "Perro"}
    )
    animal_id = create.json()["id"]
    response = client.get(f"/animals/{animal_id}")
    assert response.status_code == 200
    assert response.json()["id"] == animal_id


def test_update_animal(client):
    token = create_admin_token()
    create = client.post(
        "/animals/",
        headers={"Authorization": f"Bearer {token}"},
        data={"nombre": "Firulais", "especie": "Perro"}
    )
    animal_id = create.json()["id"]
    response = client.patch(
        f"/animals/{animal_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"nombre": "NuevoNombre"}
    )
    assert response.status_code == 200
    assert response.json()["nombre"] == "NuevoNombre"


def test_delete_animal_soft(client):
    token = create_admin_token()
    create = client.post(
        "/animals/",
        headers={"Authorization": f"Bearer {token}"},
        data={"nombre": "Firulais", "especie": "Perro"}
    )
    animal_id = create.json()["id"]
    delete = client.delete(
        f"/animals/{animal_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete.status_code == 204
    response = client.get("/animals/")
    assert response.json() == []
