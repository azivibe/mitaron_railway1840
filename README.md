# mitaron_railway1840

Auditable data pipeline for studying whether British Railway Mania railway authorisations in the 1840s were actually constructed and opened.

## MVP research target

This MVP operationalises the plan in `railway_mania_agent.md` for the 1845–1846 peak Railway Mania cohort. It joins two separately prepared tracks:

1. **Authorisation track** — HathiTrust Parliamentary Papers record `100335445` is registered in `data/sources_manifest.csv`; permitted OCR/TXT/PDF files should be manually placed under `data/raw/` before extraction.
2. **Construction track** — CAMPOP railway GIS exports should be placed under `data/external/campop_gis/`; the MVP adapter currently accepts CSV exports and normalises identifiers/names for matching.

The first analysis question is whether routes authorised in 1845–1846 were opened by 1851/1852 at lower rates than comparison cohorts.

## MVP workflow

```bash
python src/04_normalize.py \
  --input data/interim/authorized_segments_extracted.jsonl \
  --acts-out data/processed/acts.csv \
  --segments-out data/processed/authorized_segments.csv

python src/05_validate.py \
  --segments data/processed/authorized_segments.csv \
  --benchmarks config/benchmarks.yaml \
  --report logs/validation_reports/latest.json

python src/06_prepare_gis.py \
  --input data/external/campop_gis/ \
  --lines-out data/processed/lines.csv \
  --segments-out data/processed/line_segments.csv

python src/07_match.py \
  --authorized data/processed/authorized_segments.csv \
  --gis data/processed/line_segments.csv \
  --candidates-out data/interim/match_candidates.csv \
  --matches-out data/interim/auto_matches.csv

python src/09_aggregate.py \
  --authorized data/processed/authorized_segments.csv \
  --matches data/interim/auto_matches.csv \
  --out outputs/tables/cohort_summary.csv
```


## Quickstart with sample fixtures

The repository includes small synthetic fixtures for a deterministic end-to-end MVP run. They are test data only and do **not** claim to represent historical railway authorisations or CAMPOP records.

```bash
mkdir -p data/interim data/processed data/external/campop_gis outputs/tables logs/validation_reports
cp tests/fixtures/authorized_segments_extracted.jsonl data/interim/authorized_segments_extracted.jsonl
cp tests/fixtures/campop_gis_sample.csv data/external/campop_gis/campop_gis_sample.csv

python src/04_normalize.py \
  --input data/interim/authorized_segments_extracted.jsonl \
  --acts-out data/processed/acts.csv \
  --segments-out data/processed/authorized_segments.csv

python src/06_prepare_gis.py \
  --input data/external/campop_gis/ \
  --lines-out data/processed/lines.csv \
  --segments-out data/processed/line_segments.csv

python src/07_match.py \
  --authorized data/processed/authorized_segments.csv \
  --gis data/processed/line_segments.csv \
  --candidates-out data/interim/match_candidates.csv \
  --matches-out data/interim/auto_matches.csv \
  --auto-threshold 0.85

python src/09_aggregate.py \
  --authorized data/processed/authorized_segments.csv \
  --matches data/interim/auto_matches.csv \
  --out outputs/tables/cohort_summary.csv
```

The final command writes `outputs/tables/cohort_summary.csv`, including `construction_rate_1851` and `construction_rate_1852`. The matching step also preserves `data/interim/match_candidates.csv` with the top five candidate GIS rows for each authorised segment.

Real Parliamentary Papers extraction remains a later project stage. Do not scrape or mass-download restricted Parliamentary Papers databases; manually place permitted raw or extracted files under `data/` and preserve audit fields such as `source_doc_id`, `source_page`, `source_line_start`, `source_line_end`, `raw_text_excerpt`, and `confidence` when available.

## Implemented MVP components

- `src/railway_mania.py` contains deterministic normalisation, capital/length conversion, fuzzy candidate scoring, and construction-rate utilities.
- `src/04_normalize.py` converts extracted JSONL rows into auditable `acts.csv` and `authorized_segments.csv` tables.
- `src/05_validate.py` checks required columns and compares eligible authorised miles against benchmark totals in `config/benchmarks.yaml`.
- `src/06_prepare_gis.py` prepares CAMPOP-derived CSV exports as `lines.csv` and `line_segments.csv`.
- `src/07_match.py` creates top fuzzy match candidates and high-confidence automatic matches.
- `src/09_aggregate.py` produces cohort-level construction rates for 1851 and 1852.

## Data policy

Do not scrape or mass-download restricted Parliamentary Papers sources. Register each source in `data/sources_manifest.csv`, preserve raw files, and record hashes once local source files are placed.
