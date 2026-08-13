from urllib.parse import parse_qs, urlsplit

from fastapi.testclient import TestClient

from supermarkt.asgi import app
from supermarkt import access, ui


def test_home_and_static_assets():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert 'name="postal_code"' in response.text
    assert 'href="/static/home.css"' in response.text
    assert 'src="/static/home.js"' in response.text
    assert client.get("/static/home.css").status_code == 200
    assert client.get("/static/results.js").status_code == 200


def test_favicon_routes_are_local_and_cacheable():
    client = TestClient(app)
    for path in ("/favicon.svg", "/favicon.ico"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("image/svg+xml")
        assert "max-age=86400" in response.headers["cache-control"]


def test_browser_search_and_invalid_postal_code():
    client = TestClient(app)
    response = client.post("/search", data={"postal_code": "01067"}, follow_redirects=False)
    assert response.status_code == 303
    parsed = urlsplit(response.headers["location"])
    assert parsed.path == "/results/synthetic-link-test"
    assert len(parse_qs(parsed.query)["token"][0]) == 32
    bad = client.post("/search", data={"postal_code": "123"})
    assert bad.status_code == 400
    assert 'value="123"' in bad.text


def test_results_page_uses_external_assets_and_data_attributes():
    client = TestClient(app)
    response = client.get(access.build_result_path("synthetic-link-test", ("lidl_plus", "payback")))
    assert response.status_code == 200
    assert 'src="/static/results.js"' in response.text
    assert 'data-search-id="synthetic-link-test"' in response.text
    assert 'data-loyalty="lidl_plus,payback"' in response.text


def test_ui_javascript_keeps_expected_behaviour():
    script = ui.static_text("results.js")
    css = ui.static_text("results.css")
    assert "function syncLoyaltyUrl()" in script
    assert 'history.replaceState(null,"",u)' in script
    assert "Weitere Angebote werden beim Scrollen geladen" in script
    assert 'classList.toggle("single-retailer",Boolean(retailer))' in script
    assert '.table.single-retailer .retailer{display:none}' in css
