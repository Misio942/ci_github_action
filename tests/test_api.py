"""Pruebas de integración de la API Flask."""
import pytest

from app.main import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_calculate_add(client):
    resp = client.post("/calculate", json={"op": "sumar", "a": 2, "b": 3})
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 5


def test_calculate_unknown_op(client):
    resp = client.post("/calculate", json={"op": "power", "a": 2, "b": 3})
    assert resp.status_code == 400


def test_calculate_divide_by_zero(client):
    resp = client.post("/calculate", json={"op": "dividir", "a": 1, "b": 0})
    assert resp.status_code == 400


def test_calculate_bad_input(client):
    resp = client.post("/calculate", json={"op": "sumar", "a": "x", "b": 3})
    assert resp.status_code == 400
