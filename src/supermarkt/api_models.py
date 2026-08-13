from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from .common import validate_postal_code
from .loyalty import PROGRAMS, VALID_PROGRAM_IDS, normalize_program_ids


class SupermarketRequest(BaseModel):
    postal_code: str = Field(description="Deutsche Postleitzahl mit fünf Ziffern")
    aldi_region: Literal["auto", "nord", "sued"] = Field(
        default="auto",
        description="ALDI-Region. Explizite Nutzerangaben übernehmen, sonst auto.",
    )
    filter_text: str = Field(default="", max_length=120, description="Optionaler Produkt- oder Markenfilter")
    retailer: str = Field(default="", max_length=60, description="Optionaler Händlerfilter, z. B. Lidl oder Kaufland")
    page: int = Field(default=1, ge=1, le=10000)
    page_size: int = Field(default=100, ge=1, le=100, description="Maximal 100 Angebote pro API-Antwort")
    view: Literal["best_only", "all"] = Field(default="best_only", description="Nur günstigste sichere Treffer oder alle")
    loyalty_programs: list[str] = Field(
        default_factory=list,
        description=(
            "Mehrere vorhandene Bonusprogramme gleichzeitig aktivieren. Gültige IDs: "
            + ", ".join(program.id for program in PROGRAMS)
        ),
    )
    sort: Literal["price", "unit_price", "retailer", "product"] = Field(default="price")
    refresh: bool = Field(default=False, description="Servercache ignorieren und Quellen neu abrufen")

    @field_validator("postal_code")
    @classmethod
    def valid_postal_code(cls, value: str) -> str:
        normalized = validate_postal_code(value)
        if normalized is None:
            raise ValueError("Postleitzahl muss genau fünf Ziffern enthalten")
        return normalized

    @field_validator("loyalty_programs")
    @classmethod
    def valid_loyalty_programs(cls, values: list[str]) -> list[str]:
        raw = [str(value or "").strip().casefold() for value in values]
        unknown = sorted({value for value in raw if value and value not in VALID_PROGRAM_IDS})
        if unknown:
            raise ValueError("Unbekannte Bonusprogramme: " + ", ".join(unknown))
        return list(normalize_program_ids(raw))
