#!/usr/bin/env python
from __future__ import annotations
from pathlib import Path
import pandas as pd
import typer
from src.railway_mania import clean_name

app = typer.Typer()

@app.command()
def main(input: Path, lines_out: Path, segments_out: Path) -> None:
    """MVP CAMPOP adapter: normalise a supplied CSV; GIS shapefile support is a later phase."""
    csvs = sorted(input.glob("*.csv")) if input.is_dir() else [input]
    if not csvs:
        raise typer.BadParameter("place at least one CAMPOP-derived CSV in data/external/campop_gis/")
    df = pd.concat([pd.read_csv(p) for p in csvs], ignore_index=True).fillna("")
    df["line_id"] = df.get("line_id", pd.Series([f"LINE_{i+1:06d}" for i in range(len(df))]))
    df["company_name_clean"] = df.get("company_name_clean", df.get("company_name_raw", "")).map(clean_name)
    df["line_name_clean"] = df.get("line_name_clean", df.get("line_name_raw", "")).map(clean_name)
    segments = df.copy()
    segments["gis_segment_id"] = segments.get("gis_segment_id", pd.Series([f"GIS_{i+1:06d}" for i in range(len(segments))]))
    lines_out.parent.mkdir(parents=True, exist_ok=True); segments_out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(lines_out, index=False); segments.to_csv(segments_out, index=False)

if __name__ == "__main__":
    app()
