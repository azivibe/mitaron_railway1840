#!/usr/bin/env python
from __future__ import annotations
from pathlib import Path
import pandas as pd
import typer
from src.railway_mania import construction_rate

app = typer.Typer()

@app.command()
def main(authorized: Path, matches: Path, out: Path) -> None:
    auth = pd.read_csv(authorized).fillna("")
    match = pd.read_csv(matches).fillna("") if matches.exists() else pd.DataFrame()
    if not match.empty:
        auth = auth.merge(match, on="authorized_segment_id", how="left")
    auth["eligible_miles"] = auth.apply(lambda r: float(r.get("authorized_length_miles_decimal") or 0) if str(r.get("is_eligible_for_construction_rate", "")).lower() in {"true", "1"} else 0.0, axis=1)
    auth["built_by_1851_miles"] = auth.apply(lambda r: float(r["eligible_miles"]) if str(r.get("match_status", "")) == "matched" and int(float(r.get("opening_year", 9999) or 9999)) <= 1851 else 0.0, axis=1)
    auth["built_by_1852_miles"] = auth.apply(lambda r: float(r["eligible_miles"]) if str(r.get("match_status", "")) == "matched" and int(float(r.get("opening_year", 9999) or 9999)) <= 1852 else 0.0, axis=1)
    rows = []
    for year, g in auth.groupby("act_year"):
        eligible = g["eligible_miles"].sum()
        b1851 = g["built_by_1851_miles"].sum(); b1852 = g["built_by_1852_miles"].sum()
        rows.append({"act_year": int(year), "eligible_authorized_miles": eligible, "number_of_segments": len(g), "built_by_1851_miles": b1851, "built_by_1852_miles": b1852, "construction_rate_1851": construction_rate(b1851, eligible), "construction_rate_1852": construction_rate(b1852, eligible)})
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).sort_values("act_year").to_csv(out, index=False)

if __name__ == "__main__":
    app()
