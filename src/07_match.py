#!/usr/bin/env python
from __future__ import annotations
from pathlib import Path
import pandas as pd
import typer
from src.railway_mania import score_candidate

app = typer.Typer()


def _to_float(value: object) -> float | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _opening_not_before_act(act_year: object, opening_year: object) -> bool:
    act = _to_float(act_year)
    opening = _to_float(opening_year)
    return act is not None and opening is not None and int(opening) >= int(act)


@app.command()
def main(authorized: Path, gis: Path, candidates_out: Path, matches_out: Path, auto_threshold: float = 0.90) -> None:
    auth = pd.read_csv(authorized).fillna("")
    lines = pd.read_csv(gis).fillna("")
    candidates = []
    for _, a in auth.iterrows():
        scored = []
        for _, g in lines.iterrows():
            s = score_candidate(a.to_dict(), g.to_dict())
            scored.append((s.overall_score, s, g))
        for rank, (_, s, g) in enumerate(sorted(scored, key=lambda x: x[0], reverse=True)[:5], start=1):
            segment_length = g.get("segment_length_miles", "")
            line_length = g.get("line_length_miles", "")
            built_length = _to_float(segment_length) if _to_float(segment_length) is not None else _to_float(line_length)
            authorized_length = _to_float(a.get("authorized_length_miles_decimal", a.get("authorized_miles", "")))
            valid_year = _opening_not_before_act(a.get("act_year", ""), g.get("opening_year", ""))
            candidates.append({
                "candidate_id": f"CAND_{len(candidates)+1:07d}",
                "authorized_segment_id": a["authorized_segment_id"],
                "gis_segment_id": g.get("gis_segment_id", g.get("line_id", "")),
                "act_year": a.get("act_year", ""),
                "opening_year": g.get("opening_year", ""),
                "segment_length_miles": segment_length,
                "line_length_miles": line_length,
                "matched_built_miles": built_length if built_length is not None else "",
                "matched_length_ratio": (built_length / authorized_length) if built_length is not None and authorized_length and authorized_length > 0 else "",
                "company_score": s.company_score,
                "route_start_score": s.route_start_score,
                "route_end_score": s.route_end_score,
                "intermediate_place_score": s.intermediate_place_score,
                "county_score": s.county_score,
                "length_similarity_score": s.length_similarity_score,
                "year_score": s.year_score,
                "overall_score": s.overall_score,
                "candidate_rank": rank,
                "auto_match_candidate": bool(valid_year and rank == 1 and s.overall_score >= auto_threshold),
            })
    cand = pd.DataFrame(candidates)
    auto = cand[cand["auto_match_candidate"]] if not cand.empty else pd.DataFrame()
    match_rows = []
    for i, (_, r) in enumerate(auto.iterrows(), start=1):
        match_rows.append({
            "match_id": f"MATCH_{i:07d}",
            "authorized_segment_id": r["authorized_segment_id"],
            "matched_gis_segment_id": r["gis_segment_id"],
            "match_status": "matched",
            "match_method": "fuzzy_name",
            "match_confidence": r["overall_score"],
            "opening_year": r.get("opening_year", ""),
            "segment_length_miles": r.get("segment_length_miles", ""),
            "line_length_miles": r.get("line_length_miles", ""),
            "matched_built_miles": r.get("matched_built_miles", ""),
            "matched_length_ratio": r.get("matched_length_ratio", ""),
        })
    matches = pd.DataFrame(match_rows, columns=["match_id", "authorized_segment_id", "matched_gis_segment_id", "match_status", "match_method", "match_confidence", "opening_year", "segment_length_miles", "line_length_miles", "matched_built_miles", "matched_length_ratio"])
    candidates_out.parent.mkdir(parents=True, exist_ok=True); matches_out.parent.mkdir(parents=True, exist_ok=True)
    cand.to_csv(candidates_out, index=False); matches.to_csv(matches_out, index=False)

if __name__ == "__main__":
    app()
