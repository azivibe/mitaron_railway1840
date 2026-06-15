#!/usr/bin/env python
from __future__ import annotations
import json
from datetime import datetime, UTC
from pathlib import Path
import pandas as pd
import typer
import yaml

app = typer.Typer()

@app.command()
def main(segments: Path, benchmarks: Path, report: Path) -> None:
    df = pd.read_csv(segments).fillna("")
    cfg = yaml.safe_load(benchmarks.read_text())
    warnings = []
    required = ["authorized_segment_id", "act_year", "company_name_raw", "segment_type", "source_doc_id"]
    for col in required:
        if col not in df.columns:
            warnings.append({"gate": "schema", "level": "error", "message": f"missing required column: {col}"})
    if "authorized_length_miles_decimal" in df:
        totals = df[df.get("is_eligible_for_construction_rate", False).astype(str).str.lower().isin(["true", "1"])]
        for year, total in totals.groupby("act_year")["authorized_length_miles_decimal"].sum().items():
            bench = cfg.get("authorized_miles", {}).get(int(year), {}).get("odlyzko") if str(year).isdigit() else None
            if bench:
                pct = abs(total - bench) / bench * 100
                if pct > float(cfg.get("tolerance_percent", 3.0)):
                    warnings.append({"gate": "benchmark", "level": "warning", "year": int(year), "computed": total, "benchmark": bench, "percent_difference": pct})
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps({"created_at": datetime.now(UTC).isoformat(), "row_count": len(df), "warnings": warnings}, indent=2))
    if any(w["level"] == "error" for w in warnings):
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
