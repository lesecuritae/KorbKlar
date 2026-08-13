from urllib.parse import parse_qs, urlsplit

from supermarkt import access, media_routes, runtime
from supermarkt.images import ImageResult


def test_signed_image_proxy_url():
    offer={"retailer":"Lidl","product":"Testprodukt","image_url":"https://mg2de.b-cdn.net/api/v1/offers/24174643/images/default/0/medium.jpg","source_url":"https://www.marktguru.de/"}
    parsed=urlsplit(access.build_image_proxy_url(offer))
    params=parse_qs(parsed.query)
    assert parsed.path == "/image"
    assert params["src"][0] == offer["image_url"]
    assert len(params["sig"][0]) == 32


def test_image_endpoint_returns_proxy_response(monkeypatch):
    class FakeImageService:
        def get(self, **kwargs):
            return ImageResult(b"\xff\xd8\xfftest", "image/jpeg", "source")
    monkeypatch.setattr(runtime, "get_image_service", lambda: FakeImageService())
    src="https://mg2de.b-cdn.net/api/v1/offers/24174643/images/default/0/medium.jpg"
    ref="https://www.marktguru.de/"
    sig=access.image_proxy_signature(src, ref, "Testprodukt", "Lidl")
    response=media_routes.supermarket_image(src=src, ref=ref, q="Testprodukt", retailer="Lidl", sig=sig)
    assert response.media_type == "image/jpeg"
    assert response.body == b"\xff\xd8\xfftest"
