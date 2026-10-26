from unittest.mock import MagicMock

import psycopg
import pytest
from fastapi.testclient import TestClient

from app import database, main
from app.main import app

client = TestClient(app)


@pytest.fixture
def db_connection(monkeypatch):
    connection = MagicMock()
    manager = MagicMock()
    manager.__enter__.return_value = connection
    monkeypatch.setattr(main, "get_connection", lambda: manager)
    return connection


def test_list_users(db_connection):
    db_connection.execute.return_value.fetchall.return_value = [
        {"id": 7, "name": "Ada", "email": "ada@example.com", "password_hash": "secret"}
    ]
    response = client.get("/users?limit=2")
    assert response.status_code == 200
    assert response.json() == {"items": [{"id": 7, "name": "Ada", "email": "ada@example.com"}]}
    query, params = db_connection.execute.call_args.args
    assert params == (2,)
    assert "ORDER BY id LIMIT %s" in query
    assert "password_hash" not in query and "SELECT *" not in query


def test_get_user(db_connection):
    db_connection.execute.return_value.fetchone.return_value = {
        "id": 7,
        "name": "Ada",
        "email": "ada@example.com",
    }
    response = client.get("/users/7")
    assert response.status_code == 200
    assert response.json()["id"] == 7
    query, params = db_connection.execute.call_args.args
    assert "WHERE id = %s" in query
    assert params == (7,)


def test_missing_user(db_connection):
    db_connection.execute.return_value.fetchone.return_value = None
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.parametrize("url", ["/users/abc", "/users?limit=0", "/users?limit=101"])
def test_invalid_input(url, db_connection):
    assert client.get(url).status_code == 422
    db_connection.execute.assert_not_called()


def test_db_failure_is_not_not_found(db_connection):
    db_connection.execute.side_effect = psycopg.OperationalError("unavailable")
    with TestClient(app, raise_server_exceptions=False) as safe_client:
        assert safe_client.get("/users/1").status_code == 500


def test_connection_configuration(monkeypatch):
    for key, value in {
        "PGHOST": "pooler.example.com",
        "PGUSER": "postgres.test",
        "PGDATABASE": "postgres",
        "PGPASSWORD": "test-password",
        "PGPORT": "5432",
    }.items():
        monkeypatch.setenv(key, value)
    connect = MagicMock()
    monkeypatch.setattr(database.psycopg, "connect", connect)
    database.get_connection()
    assert connect.call_args.kwargs["sslmode"] == "require"
    assert connect.call_args.kwargs["connect_timeout"] == 5
    assert connect.call_args.kwargs["port"] == 5432


def test_missing_configuration(monkeypatch):
    monkeypatch.delenv("PGHOST", raising=False)
    with pytest.raises(RuntimeError, match="PGHOST"):
        database.get_connection()


def test_create_user(db_connection):
    db_connection.execute.return_value.fetchone.return_value = {
        "id": 8,
        "name": "Ada",
        "email": "ada@example.com",
    }
    response = client.post("/users", json={"name": " Ada ", "email": "ADA@example.com"})
    assert response.status_code == 201
    assert response.json() == {"id": 8, "name": "Ada", "email": "ada@example.com"}
    assert db_connection.execute.call_args.args[1] == ("Ada", "ada@example.com", "!dummy-no-login")


@pytest.mark.parametrize("constraint,status", [("users_email_key", 409), ("other_key", 500)])
def test_create_unique_violation(db_connection, constraint, status):
    class Duplicate(psycopg.errors.UniqueViolation):
        @property
        def diag(self):
            return type("Diagnostic", (), {"constraint_name": constraint})()

    db_connection.execute.side_effect = Duplicate("duplicate")
    with TestClient(app, raise_server_exceptions=False) as safe_client:
        response = safe_client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    assert response.status_code == status


@pytest.mark.parametrize(
    "body", [{}, {"name": " "}, {"name": None}, {"name": "A", "email": "a@example.com"}]
)
def test_patch_invalid_body(db_connection, body):
    assert client.patch("/users/7", json=body).status_code == 422
    db_connection.execute.assert_not_called()


def test_patch_user(db_connection):
    db_connection.execute.return_value.fetchone.return_value = {
        "id": 7,
        "name": "Grace",
        "email": "ada@example.com",
    }
    response = client.patch("/users/7", json={"name": " Grace "})
    assert response.status_code == 200
    assert response.json() == {"id": 7, "name": "Grace", "email": "ada@example.com"}
    assert db_connection.execute.call_args.args[1] == ("Grace", 7)


def test_delete_user(db_connection):
    db_connection.execute.return_value.fetchone.return_value = {"id": 7}
    response = client.delete("/users/7")
    assert response.status_code == 204
    assert response.content == b""
    assert db_connection.execute.call_args.args[1] == (7,)


@pytest.mark.parametrize("method,kwargs", [("patch", {"json": {"name": "Ada"}}), ("delete", {})])
def test_write_missing_user(db_connection, method, kwargs):
    db_connection.execute.return_value.fetchone.return_value = None
    response = getattr(client, method)("/users/999", **kwargs)
    assert response.status_code == 404


@pytest.mark.parametrize(
    "body",
    [
        {"name": "Ada", "email": "invalid"},
        {"name": " ", "email": "ada@example.com"},
        {"name": "Ada", "email": "ada@example.com", "id": 1},
    ],
)
def test_create_invalid_body(db_connection, body):
    assert client.post("/users", json=body).status_code == 422
    db_connection.execute.assert_not_called()
