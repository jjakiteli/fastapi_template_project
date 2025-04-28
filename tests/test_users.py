from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from main import app
from roles.dependencies import (
    DeleteUserPermission,
    ReadUserPermission,
    UpdateUserPermission,
)
from security.dependencies import OAuth, create_access_token
from users.dependencies import get_current_user, get_user_repo
from users.models import UserCreate, UserDB, UserDeleted, UserRead, UserUpdate


class MockUserRepo:
    async def get_all_users(self):
        return [
            UserRead(
                id=1,
                username="alice",
                description="test user",
                role="user",
                is_active=True,
                last_active=datetime.now(),
            )
        ]

    async def get_user(self, id: int):
        return UserRead(
            id=id,
            username=f"user{id}",
            description="some user",
            role="user",
            is_active=True,
            last_active=datetime.now(),
        )

    async def get_user_by_username(self, username: str):
        return UserDB(
            id=1,
            username=username,
            password="password",
            description="some user",
            role="user",
            is_active=True,
            last_active=datetime.now(),
        )

    async def create_user(self, user: UserCreate):
        return UserRead(
            id=2,
            username=user.username,
            description=user.description,
            role=None,
            is_active=True,
            last_active=datetime.now(),
        )

    async def update_user(self, id: int, user: UserUpdate):
        return UserRead(
            id=id,
            username=user.username,
            description=user.description,
            role="user",
            is_active=True,
            last_active=datetime.now(),
        )

    async def delete_user(self, id: int):
        return UserDeleted(
            id=id,
            username=f"user{id}",
            description="deleted user",
            role="user",
            is_active=False,
            last_active=datetime.now(),
        )

    async def edit_user_role(self, id: int, role: str):
        return UserRead(
            id=id,
            username=f"user{id}",
            description="role changed",
            role=role,
            is_active=True,
            last_active=datetime.now(),
        )


class MockOAuth:
    def __init__(self):
        self.token = "mocked-token"
        self.user_id = 1


class MockCurrentUser:
    id = 1
    username = "me"
    description = "current user"
    role = "root"
    is_active = True
    last_active = datetime.now()


app.dependency_overrides[get_user_repo] = lambda: MockUserRepo()
app.dependency_overrides[OAuth] = lambda: MockOAuth()
app.dependency_overrides[get_current_user] = lambda: MockCurrentUser()
app.dependency_overrides[ReadUserPermission] = lambda: None
app.dependency_overrides[UpdateUserPermission] = lambda: None
app.dependency_overrides[DeleteUserPermission] = lambda: None
client = TestClient(app)


def generate_valid_token():
    data = {"sub": "testuser"}
    return create_access_token(data, expires_delta=timedelta(minutes=15))


token = generate_valid_token()
headers = {"Authorization": f"Bearer {token}"}


def test_get_all_users():
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["username"] == "alice"


def test_get_user():
    response = client.get("/users/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_me():
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "me"
    assert data["role"] == "root"


def test_create_user():
    payload = {
        "username": "johndoe",
        "password": "secure123",
        "description": "A test user",
    }
    response = client.post("/users/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"


def test_update_me():
    payload = {
        "username": "updateduser",
        "password": "newpassword",
        "description": "Updated description",
    }
    response = client.put("/users/me", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"


def test_update_user():
    payload = {
        "username": "updated2",
        "password": "pass123",
        "description": "Another update",
    }
    response = client.put("/users/2", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == 2


def test_edit_user_role():
    response = client.patch("/users/3/role?role=admin", headers=headers)
    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_delete_me():
    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert not response.json()["is_active"]


def test_delete_user():
    response = client.delete("/users/4", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == 4
