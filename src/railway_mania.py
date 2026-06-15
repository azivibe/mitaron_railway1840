"""Core MVP utilities for Railway Mania authorisation/construction analysis."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

try:
    from rapidfuzz import fuzz
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal test environments
    from difflib import SequenceMatcher

    class _Fuzz:
        @staticmethod
        def token_sort_ratio(left: str, right: str) -> float:
            a = " ".join(sorted(left.split()))
            b = " ".join(sorted(right.split()))
            return SequenceMatcher(None, a, b).ratio() * 100

    fuzz = _Fuzz()

ELIGIBLE_SEGMENT_TYPES = {"new_line", "branch", "extension", "deviation"}


def clean_name(value: object) -> str:
    """Normalise a company/place name while preserving meaningful tokens."""
    if value is None:
        return ""
    text = str(value).lower().replace("&", " and ")
    text = re.sub(r"\brailway\b|\brailroad\b|\bcompany\b|\bthe\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def length_to_decimal(miles: object = 0, chains: object = 0) -> float | None:
    """Convert miles/chains to decimal miles; 80 chains equal one mile."""
    if miles in (None, "") and chains in (None, ""):
        return None
    return float(miles or 0) + float(chains or 0) / 80.0


def parse_pounds(value: object) -> int | None:
    """Parse common nineteenth-century pound formats into integer pounds."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value)
    digits = re.sub(r"[^0-9]", "", text)
    return int(digits) if digits else None


def eligible_for_construction_rate(segment_type: object, explicit: object = None) -> bool:
    """Apply denominator rule for construction-realisation calculations."""
    if explicit is not None and str(explicit).strip() != "":
        return str(explicit).strip().lower() in {"1", "true", "yes", "y"}
    return str(segment_type or "").strip() in ELIGIBLE_SEGMENT_TYPES


def similarity(left: object, right: object) -> float:
    """Token-sort similarity on cleaned names, scaled 0-1."""
    a = clean_name(left)
    b = clean_name(right)
    if not a or not b:
        return 0.0
    return fuzz.token_sort_ratio(a, b) / 100.0


def overlap_score(left: object, right: object) -> float:
    """Simple set overlap for comma/semicolon-delimited places or counties."""
    def tokens(value: object) -> set[str]:
        if value is None:
            return set()
        return {clean_name(part) for part in re.split(r"[,;|]", str(value)) if clean_name(part)}

    a, b = tokens(left), tokens(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def length_score(authorized_miles: object, built_miles: object) -> float:
    """Return 1 for equal lengths, declining linearly to 0 at 100% difference."""
    try:
        a = float(authorized_miles)
        b = float(built_miles)
    except (TypeError, ValueError):
        return 0.0
    if a <= 0 or b <= 0:
        return 0.0
    return max(0.0, 1.0 - abs(a - b) / max(a, b))


def year_score(act_year: object, opening_year: object) -> float:
    """Reward plausible post-authorisation opening years."""
    try:
        act = int(act_year)
        opening = int(opening_year)
    except (TypeError, ValueError):
        return 0.0
    if opening < act:
        return 0.0
    lag = opening - act
    if lag <= 6:
        return 1.0
    if lag <= 15:
        return 0.7
    return 0.4


@dataclass(frozen=True)
class MatchScores:
    company_score: float
    route_start_score: float
    route_end_score: float
    intermediate_place_score: float
    county_score: float
    length_similarity_score: float
    year_score: float
    overall_score: float


def score_candidate(authorized: dict, gis: dict, weights: dict[str, float] | None = None) -> MatchScores:
    """Score one authorised segment against one GIS segment."""
    weights = weights or {
        "company_score": 0.25,
        "endpoint_score": 0.25,
        "intermediate_place_score": 0.15,
        "county_score": 0.15,
        "length_score": 0.10,
        "year_score": 0.10,
    }
    company = similarity(authorized.get("company_name_clean") or authorized.get("company_name_raw"), gis.get("company_name_clean") or gis.get("company_name_raw"))
    start = similarity(authorized.get("route_start_clean") or authorized.get("route_start_raw"), gis.get("segment_start") or gis.get("route_start_clean"))
    end = similarity(authorized.get("route_end_clean") or authorized.get("route_end_raw"), gis.get("segment_end") or gis.get("route_end_clean"))
    endpoint = (start + end) / 2.0
    intermediate = overlap_score(authorized.get("intermediate_places_clean") or authorized.get("intermediate_places_raw"), gis.get("nearest_towns") or gis.get("intermediate_places"))
    county = overlap_score(authorized.get("counties_clean") or authorized.get("counties_raw"), gis.get("county") or gis.get("counties"))
    length = length_score(authorized.get("authorized_length_miles_decimal") or authorized.get("authorized_miles"), gis.get("segment_length_miles") or gis.get("line_length_miles"))
    year = year_score(authorized.get("act_year"), gis.get("opening_year"))
    overall = (
        weights["company_score"] * company
        + weights["endpoint_score"] * endpoint
        + weights["intermediate_place_score"] * intermediate
        + weights["county_score"] * county
        + weights["length_score"] * length
        + weights["year_score"] * year
    )
    return MatchScores(company, start, end, intermediate, county, length, year, overall)


def construction_rate(built_miles: float, eligible_miles: float) -> float | None:
    """Calculate built miles over eligible authorised miles."""
    if eligible_miles == 0:
        return None
    return built_miles / eligible_miles
