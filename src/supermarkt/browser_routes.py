from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from .access import build_result_path, verify_result_token
from .assets import FAVICON_SVG
from .common import clean_text, validate_postal_code
from .loyalty import normalize_program_ids
from .models import ToolError
from . import runtime
from .ui import build_home_html, build_results_html

router = APIRouter()


@router.get("/favicon.svg", include_in_schema=False)
def favicon_svg() -> Response:
    return Response(content=FAVICON_SVG, media_type="image/svg+xml", headers={"Cache-Control": "public, max-age=86400", "X-Content-Type-Options": "nosniff"})


@router.get("/favicon.ico", include_in_schema=False)
def favicon_ico() -> Response:
    return favicon_svg()


@router.get("/", include_in_schema=False, response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse(build_home_html(), headers={"Cache-Control": "no-store"})


@router.post("/search", include_in_schema=False)
def browser_search(postal_code_input: Annotated[str, Form(alias="postal_code")] = "") -> Response:
    raw_postal_code = clean_text(postal_code_input)
    postal_code = validate_postal_code(raw_postal_code)
    if postal_code is None:
        return HTMLResponse(build_home_html(error="Bitte eine gültige fünfstellige deutsche Postleitzahl eingeben.", postal_code=raw_postal_code), status_code=400, headers={"Cache-Control": "no-store"})
    try:
        snapshot, _ = runtime.get_engine().snapshot(postal_code, "auto", False)
    except ToolError as exc:
        return HTMLResponse(build_home_html(error=str(exc), postal_code=postal_code), status_code=502, headers={"Cache-Control": "no-store"})
    return RedirectResponse(build_result_path(snapshot["search_id"]), status_code=303)


@router.get("/results/{search_id}", include_in_schema=False, response_class=HTMLResponse, name="supermarket_results")
def results_page(search_id: str, token: str = Query(default=""), loyalty: str = Query(default="", max_length=500)) -> HTMLResponse:
    verify_result_token(search_id, token)
    try:
        runtime.get_engine().by_id(search_id)
    except ToolError as exc:
        raise HTTPException(status_code=410, detail=str(exc)) from exc
    selected = normalize_program_ids(loyalty.split(","))
    return HTMLResponse(build_results_html(search_id, token, selected), headers={"Cache-Control": "no-store"})
