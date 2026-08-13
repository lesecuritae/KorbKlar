from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from .config import CACHE_TTL_MINUTES
from .security import api_key
from . import runtime

router = APIRouter()


@router.get("/health", include_in_schema=False)
def health() -> dict[str, Any]:
    engine = runtime.get_engine()
    return {
        "status": "ok",
        "service": "korbklar",
        "backend": "persistent-sqlite-cache",
        "cache_ttl_minutes": CACHE_TTL_MINUTES,
        "api_auth_configured": bool(api_key()),
        **runtime.get_image_service().health(),
        "sources": {
            "REWE": "official primary with Marktguru fallback",
            "EDEKA": "official primary with Marktguru fallback",
            "Kaufland": "official primary with Marktguru fallback",
            "Marktkauf": "official primary with Marktguru fallback",
            "ALDI": "official primary with Marktguru fallback",
            "Lidl": "Marktguru regional catalogue",
            "PENNY": "Marktguru regional catalogue",
            "Netto": "Marktguru regional catalogue",
            "Globus": "Marktguru regional catalogue",
        },
        **engine.store.health(),
    }
