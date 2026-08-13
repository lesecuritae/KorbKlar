from urllib.parse import parse_qs, urlsplit

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from supermarkt.asgi import app
from supermarkt.api_models import SupermarketRequest


def test_api_returns_one_absolute_result_url():
    client = TestClient(app, base_url="https://offers.example.test")
    result = client.post("/api/v1/compare", json={"postal_code": "01067"}).json()
    assert result["result_url"].startswith("https://offers.example.test/results/synthetic-link-test?token=")
    assert "full_offer_list_url" not in result and "ui_url" not in result


def test_api_preserves_loyalty_programs_and_optional_auth(monkeypatch):
    client = TestClient(app, base_url="https://offers.example.test")
    response = client.post("/api/v1/compare", json={"postal_code": "01067", "loyalty_programs": ["lidl_plus", "kaufland_xtra", "payback"]})
    assert parse_qs(urlsplit(response.json()["result_url"]).query)["loyalty"] == ["lidl_plus,kaufland_xtra,payback"]
    monkeypatch.setenv("SUPERMARKT_API_KEY", "correct-key")
    assert client.post("/api/v1/compare", json={"postal_code": "01067"}).status_code == 401
    assert client.post("/api/v1/compare", json={"postal_code": "01067"}, headers={"Authorization": "Bearer correct-key"}).status_code == 200


def test_request_rejects_unknown_loyalty_program():
    with pytest.raises(ValidationError):
        SupermarketRequest(postal_code="01067", loyalty_programs=["nicht_echt"])


def test_openapi_exposes_only_compare_operation():
    operations=[]
    for path, methods in app.openapi()["paths"].items():
        for method, operation in methods.items():
            if method.lower() in {"get", "post", "put", "patch", "delete"}:
                operations.append((method.lower(), path, operation.get("operationId")))
    assert operations == [("post", "/api/v1/compare", "supermarkt_preisvergleich")]
