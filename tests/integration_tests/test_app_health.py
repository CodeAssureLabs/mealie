from fastapi.testclient import TestClient


def test_app_health(api_client: TestClient):
    response = api_client.get("/api/app/health")
    assert response.status_code == 200

    as_dict = response.json()
    assert as_dict["message"] == "ok"
    assert as_dict["error"] is False
