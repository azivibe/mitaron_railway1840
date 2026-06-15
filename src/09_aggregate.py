#!/usr/bin/env python
from __future__ import annotations
from pathlib import Path
import pandas as pd
import typer
from src.railway_mania import construction_rate

app = typer.Typer()


def _to_float(value: object, default: float = 0.0) -> float:
    try:
        if value is None or str(value).strip() == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _opening_year(value: object) -> int | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _is_eligible(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


@app.command()
def main(authorized: Path, matches: Path, out: Path) -> None:
    auth = pd.read_csv(authorized).fillna("")
    match = pd.read_csv(matches).fillna("") if matches.exists() else pd.DataFrame()
    if not match.empty:
        auth = auth.merge(match, on="authorized_segment_id", how="left")
    else:
        auth["match_status"] = ""
        auth["opening_year"] = ""
        auth["matched_built_miles"] = ""

    auth["eligible_miles"] = auth.apply(
        lambda r: _to_float(r.get("authorized_length_miles_decimal")) if _is_eligible(r.get("is_eligible_for_construction_rate", "")) else 0.0,
        axis=1,
    )

    def built_miles_by(row: pd.Series, year: int) -> float:
        if str(row.get("match_status", "")) != "matched":
            return 0.0
        opening = _opening_year(row.get("opening_year", ""))
        if opening is None or opening > year:
            return 0.0
        matched_built = row.get("matched_built_miles", "")
        return _to_float(matched_built, default=_to_float(row.get("eligible_miles", 0.0))) if str(matched_built).strip() != "" else _to_float(row.get("eligible_miles", 0.0))

    auth["built_by_1851_miles"] = auth.apply(lambda r: built_miles_by(r, 1851), axis=1)
    auth["built_by_1852_miles"] = auth.apply(lambda r: built_miles_by(r, 1852), axis=1)
    auth["is_matched_segment"] = auth["match_status"].eq("matched")
    auth["is_ambiguous_or_unmatched"] = ~auth["is_matched_segment"]
    if "match_status" in auth:
        auth.loc[auth["match_status"].astype(str).str.contains("ambiguous|unmatched", case=False, na=False), "is_ambiguous_or_unmatched"] = True

    rows = []
    for year, g in auth.groupby("act_year", dropna=False):
        eligible = g["eligible_miles"].sum()
        b1851 = g["built_by_1851_miles"].sum(); b1852 = g["built_by_1852_miles"].sum()
        rows.append({
            "act_year": int(float(year)),
            "eligible_authorized_miles": eligible,
            "built_by_1851_miles": b1851,
            "built_by_1852_miles": b1852,
            "construction_rate_1851": construction_rate(b1851, eligible),
            "construction_rate_1852": construction_rate(b1852, eligible),
            "number_of_segments": len(g),
            "number_matched_segments": int(g["is_matched_segment"].sum()),
            "ambiguous_or_unmatched_segments": int(g["is_ambiguous_or_unmatched"].sum()),
        })
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).sort_values("act_year").to_csv(out, index=False)

if __name__ == "__main__":
    app()
