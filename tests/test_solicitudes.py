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


def create_user_token(email="user@test.com", nombre="User"):
    db = TestingSessionLocal()
    user = Usuario(
        nombre=nombre,
        email=email,
        password_hash=hash_password("123456"),
        rol=UserRole.adoptante
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id), "rol": user.rol.value})
    db.close()
    return token


def create_animal(client, admin_token, **kwargs):
    data = {"nombre": "Firulais", "especie": "Perro", **kwargs}
    response = client.post(
        "/animals/",
        headers={"Authorization": f"Bearer {admin_token}"},
        data=data
    )
    return response.json()


def test_create_solicitud_success(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    user_token = create_user_token()

    response = client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id_animal"] == animal["id"]
    assert data["estado"] == "pendiente"


def test_create_solicitud_no_auth(client):
    response = client.post("/solicitudes/", json={"id_animal": 1})
    assert response.status_code == 401


def test_create_solicitud_animal_not_found(client):
    user_token = create_user_token()
    response = client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": 9999}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Animal no encontrado"


def test_create_solicitud_duplicate(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    user_token = create_user_token()

    client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    )
    response = client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Ya enviaste una solicitud para este animal"


def test_create_solicitud_pending_exists(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    token1 = create_user_token(email="user1@test.com", nombre="User1")
    token2 = create_user_token(email="user2@test.com", nombre="User2")

    client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {token1}"},
        json={"id_animal": animal["id"]}
    )
    response = client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {token2}"},
        json={"id_animal": animal["id"]}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Ya existe una solicitud pendiente para este animal"


def test_mis_solicitudes(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    user_token = create_user_token()

    client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    )
    response = client.get(
        "/solicitudes/mias",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id_animal"] == animal["id"]


def test_mis_solicitudes_no_auth(client):
    response = client.get("/solicitudes/mias")
    assert response.status_code == 401


def test_list_solicitudes_admin(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    user_token = create_user_token()

    client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    )
    response = client.get(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_list_solicitudes_not_admin(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    user_token = create_user_token()

    client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    )
    response = client.get(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403


def test_update_solicitud_approve(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    user_token = create_user_token()

    solicitud = client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    ).json()

    response = client.put(
        f"/solicitudes/{solicitud['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"estado": "aprobada"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "aprobada"


def test_update_solicitud_reject(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    user_token = create_user_token()

    solicitud = client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    ).json()

    response = client.put(
        f"/solicitudes/{solicitud['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"estado": "rechazada"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "rechazada"


def test_update_solicitud_not_admin(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    user_token = create_user_token()

    solicitud = client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    ).json()

    response = client.put(
        f"/solicitudes/{solicitud['id']}",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"estado": "aprobada"}
    )
    assert response.status_code == 403


def test_update_solicitud_not_found(client):
    admin_token = create_admin_token()
    response = client.put(
        "/solicitudes/9999",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"estado": "aprobada"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitud no encontrada"


def test_create_solicitud_post_approval(client):
    admin_token = create_admin_token()
    animal = create_animal(client, admin_token)
    user_token = create_user_token()

    solicitud = client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    ).json()

    client.put(
        f"/solicitudes/{solicitud['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"estado": "aprobada"}
    )

    response = client.post(
        "/solicitudes/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"id_animal": animal["id"]}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "El animal no está disponible"
