#!/usr/bin/env python
from __future__ import annotations
from pathlib import Path
import pandas as pd
import typer
from src.railway_mania import score_candidate

app = typer.Typer()

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
            candidates.append({
                "candidate_id": f"CAND_{len(candidates)+1:07d}", "authorized_segment_id": a["authorized_segment_id"],
                "gis_segment_id": g.get("gis_segment_id", g.get("line_id", "")), "act_year": a.get("act_year", ""), "opening_year": g.get("opening_year", ""),
                "company_score": s.company_score, "route_start_score": s.route_start_score, "route_end_score": s.route_end_score,
                "intermediate_place_score": s.intermediate_place_score, "county_score": s.county_score, "length_similarity_score": s.length_similarity_score,
                "year_score": s.year_score, "overall_score": s.overall_score, "candidate_rank": rank, "auto_match_candidate": s.overall_score >= auto_threshold,
            })
    cand = pd.DataFrame(candidates)
    auto = cand[(cand["candidate_rank"] == 1) & (cand["auto_match_candidate"])] if not cand.empty else pd.DataFrame()
    matches = pd.DataFrame({
        "match_id": [f"MATCH_{i+1:07d}" for i in range(len(auto))],
        "authorized_segment_id": auto.get("authorized_segment_id", []),
        "matched_gis_segment_id": auto.get("gis_segment_id", []),
        "match_status": "matched", "match_method": "fuzzy_name", "match_confidence": auto.get("overall_score", []),
    })
    candidates_out.parent.mkdir(parents=True, exist_ok=True); matches_out.parent.mkdir(parents=True, exist_ok=True)
    cand.to_csv(candidates_out, index=False); matches.to_csv(matches_out, index=False)

if __name__ == "__main__":
    app()
