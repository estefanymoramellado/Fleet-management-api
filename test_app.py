import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_taxis_responde_200(client):
    response = client.get("/taxis")
    assert response.status_code == 200


def test_get_taxis_devuelve_lista(client):
    response = client.get("/taxis")
    data = response.get_json()
    assert isinstance(data, list)


def test_cada_taxi_tiene_id_y_plate(client):
    response = client.get("/taxis")
    data = response.get_json()
    assert len(data) > 0 
    for taxi in data:
        assert "id" in taxi
        assert "plate" in taxi


def test_paginacion_limita_resultados(client):
    response = client.get("/taxis?limit=5")
    data = response.get_json()
    assert len(data) <= 5


def test_filtro_por_plate(client):
    response = client.get("/taxis?plate=GH")
    data = response.get_json()
    for taxi in data:
        assert "GH" in taxi["plate"].upper()