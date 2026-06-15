#!/usr/bin/env python
from __future__ import annotations
import json
from pathlib import Path
import typer
import pandas as pd
from src.railway_mania import clean_name, eligible_for_construction_rate, length_to_decimal, parse_pounds

app = typer.Typer()

@app.command()
def main(input: Path, acts_out: Path, segments_out: Path) -> None:
    rows = [json.loads(line) for line in input.read_text().splitlines() if line.strip()]
    segs = pd.DataFrame(rows)
    if segs.empty:
        raise typer.BadParameter("input contains no JSONL rows")
    segs["company_name_clean"] = segs.get("company_name_clean", segs.get("company_name_raw", "")).map(clean_name)
    segs["route_start_clean"] = segs.get("route_start_clean", segs.get("route_start_raw", "")).map(clean_name)
    segs["route_end_clean"] = segs.get("route_end_clean", segs.get("route_end_raw", "")).map(clean_name)
    segs["authorized_length_miles_decimal"] = [length_to_decimal(m, c) for m, c in zip(segs.get("authorized_miles", 0), segs.get("authorized_chains", 0))]
    if "authorized_capital_pounds" in segs:
        segs["total_authorized_capital"] = segs["authorized_capital_pounds"].map(parse_pounds)
    segs["is_eligible_for_construction_rate"] = [eligible_for_construction_rate(t, e) for t, e in zip(segs.get("segment_type", "unknown"), segs.get("is_eligible_for_construction_rate", ""))]
    segs.insert(0, "authorized_segment_id", [f"AUTH_{i+1:06d}" for i in range(len(segs))])
    segs["act_id"] = segs.get("act_id", segs["authorized_segment_id"].str.replace("AUTH", "ACT", regex=False))
    acts_cols = [c for c in ["act_id", "act_year", "session_year", "act_title_raw", "company_name_raw", "company_name_clean", "source_doc_id"] if c in segs]
    acts = segs[acts_cols].drop_duplicates("act_id") if acts_cols else pd.DataFrame()
    acts_out.parent.mkdir(parents=True, exist_ok=True); segments_out.parent.mkdir(parents=True, exist_ok=True)
    acts.to_csv(acts_out, index=False); segs.to_csv(segments_out, index=False)

if __name__ == "__main__":
    app()
