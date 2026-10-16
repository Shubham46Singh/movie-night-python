
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_ok_when_dependencies_are_healthy():
    with (
        patch("app.main.db.query") as mock_query,
        patch("app.main.cache.client") as mock_client,
    ):
        mock_query.return_value = [{"result": 1}]
        mock_client.return_value.ping.return_value = True

        client = TestClient(app)
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["postgres"] is True
    assert response.json()["redis"] is True
