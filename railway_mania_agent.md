# Railway Mania Data Pipeline — Codex / Agent Specification

## 0. Project Purpose

This repository builds an auditable data pipeline for studying the British Railway Mania of the 1840s.

The core research question is:

> Did Parliamentary railway authorisations during the peak of Railway Mania actually turn into constructed/opened railway lines, or were many of them speculative plans with low feasibility?

Japanese formulation of the hypothesis:

> **仮説：Railway Mania の絶頂期に認可された鉄道計画は、非絶頂期に認可された計画に比べて、実際の建設・開通へ転換される比率が低かった可能性がある。すなわち、バブル絶頂期の認可には、現実性や事業性の低い計画がより多く含まれていたと考えられる。**

The pipeline must convert Parliamentary Papers / Railway Acts data into structured authorisation records, match those records to actual constructed railway lines from CAMPOP GIS or equivalent railway GIS data, and calculate construction-realisation rates by authorisation year.

The final research output should allow graphs such as:

1. Railway stock index vs. authorised railway miles.
2. Authorised miles vs. actual railway investment.
3. Authorisation-year cohort vs. construction/opening rate by 1851 / 1852 / 1861.
4. Peak-bubble cohort vs. non-peak cohort construction realisation.
5. Authorised miles split into built vs. not built.
6. Optional: capital-weighted construction realisation.

---

## 1. Conceptual Design

Use two independent tracks and join them only at the matching stage.

```text
Track A — Authorisation Data
Parliamentary Papers / Railway Acts
→ OCR/TXT source
→ bill/act/route segmentation
→ LLM structured extraction
→ schema + benchmark validation
→ authorised railway table

Track B — Construction Data
CAMPOP GIS or equivalent railway GIS
→ line geometries and opening years
→ line/segment table
→ normalised construction table

Join Stage
Authorised routes + Constructed/opened lines
→ fuzzy matching + year/place/length checks
→ LLM/manual adjudication only for ambiguous cases
→ matches.csv
→ cohort-level realisation rates
```

Key methodological principle:

> Existing literature often uses annual aggregate authorised miles. This project goes below aggregate totals and checks individual authorisations against actual construction/opening outcomes.

---

## 2. Scope

Design the code to support broad coverage, but implement in phases.

### MVP Scope

```text
Authorisation years: 1845–1846
Reason: peak Railway Mania years.
Outcome check: built/opened by 1851 and 1852.
```

### Standard Paper Scope

```text
Authorisation years: 1844–1847
Reason: early mania, peak mania, and immediate post-peak cohort.
Outcome check: built/opened by 1851 and 1852.
```

### Extended Scope

```text
Authorisation years: 1840–1850 or 1830–1850
Reason: longer comparison and historical background.
Outcome check: built/opened by 1851, 1852, 1861.
```

The pipeline should be generic enough to ingest additional years later.

---

## 3. Repository Structure

Create the repository as follows.

```text
railway-mania/
├── README.md
├── AGENTS.md                         # this instruction file or a shortened version
├── pyproject.toml
├── requirements.txt
├── .env.example
├── config/
│   ├── benchmarks.yaml
│   ├── matching.yaml
│   ├── schemas/
│   │   ├── source_manifest.schema.json
│   │   ├── act.schema.json
│   │   ├── authorized_segment.schema.json
│   │   ├── line.schema.json
│   │   ├── match.schema.json
│   │   └── cohort_summary.schema.json
│   └── prompts/
│       ├── extract_authorized_segment.md
│       └── adjudicate_match.md
├── data/
│   ├── raw/                          # raw OCR/TXT/PDF; never modify
│   ├── interim/                      # intermediate jsonl files
│   ├── external/                     # CAMPOP GIS shapefiles, external CSVs
│   ├── processed/                    # final CSV/Parquet tables
│   └── sources_manifest.csv
├── logs/
│   ├── extraction_runs/
│   ├── validation_reports/
│   └── matching_reports/
├── outputs/
│   ├── tables/
│   ├── figures/
│   └── maps/
├── src/
│   ├── 00_fetch.py                   # optional public-source fetch only
│   ├── 01_prepare_text.py            # PDF/TXT → page_text.jsonl
│   ├── 02_segment.py                 # page text → bill/row/chunk records
│   ├── 03_extract.py                 # LLM extraction → JSONL
│   ├── 04_normalize.py               # names, units, dates, capital values
│   ├── 05_validate.py                # schema + benchmark validation
│   ├── 06_prepare_gis.py             # CAMPOP GIS → lines.csv / line_segments.csv
│   ├── 07_match.py                   # fuzzy candidate generation + auto matching
│   ├── 08_adjudicate.py              # LLM/manual adjudication for ambiguous cases
│   ├── 09_aggregate.py               # cohort construction rates
│   └── 10_plot.py                    # optional charts
└── tests/
    ├── test_normalize.py
    ├── test_validate.py
    ├── test_match.py
    └── gold/
        └── manually_coded_sample.csv
```

---

## 4. Package Requirements

Use Python 3.11+.

Recommended libraries:

```text
pandas
numpy
pyarrow
pydantic
jsonschema
rapidfuzz
geopandas
shapely
pyproj
fiona
python-dotenv
typer
rich
tqdm
matplotlib
pytest
```

Optional OCR/PDF tools if raw materials are scanned PDFs:

```text
pypdf
pdfplumber
pytesseract
opencv-python
Pillow
```

Do not require OCR if high-quality TXT is already available.

---

## 5. Data Inputs

### 5.1 Parliamentary Papers / Authorisation Sources

Primary source target:

```text
Return of Railway Acts, 1844–47
Parliamentary Papers, 1847–48, no. 731, vol. LXIII, pp. 275–305 or relevant pages.
```

Other relevant Parliamentary Papers may be added later.

Important rule:

> Do not scrape or mass-download from proprietary databases such as ProQuest unless the user explicitly confirms permission. If the source comes from a library database, assume manual download and local placement under `data/raw/`.

### 5.2 CAMPOP GIS / Construction Sources

Input expected under:

```text
data/external/campop_gis/
```

Expected attributes, if available:

```text
company name
line name
route / segment name
opening year
opening date
geometry
line length
```

If attributes differ, write a mapping file and document it.

### 5.3 Supporting Aggregate Sources

Optional but useful:

```text
railway stock index data
railway investment data
annual authorised miles benchmark data
```

These are used for validation and background graphs, not as replacements for route-level Parliamentary extraction.

---

## 6. Core Tables and Data Contracts

### 6.1 `sources_manifest.csv`

Purpose: audit trail for every source file.

Required columns:

```text
source_doc_id
title
year
parliamentary_session
paper_number
volume
source_type
archive_or_database
url_or_database_note
local_path
download_method
download_date
file_hash_sha256
ocr_status
notes
```

Rules:

- Every raw file must have one row.
- Raw files must never be edited.
- Record file hash after download or placement.

---

### 6.2 `page_text.jsonl`

Purpose: page-level text extracted from raw TXT/PDF/OCR.

JSONL schema:

```json
{
  "source_doc_id": "PP_RETURN_ACTS_1844_47",
  "page": 30,
  "page_label": "30",
  "text": "...",
  "ocr_confidence": null,
  "text_hash": "sha256..."
}
```

---

### 6.3 `segments_raw.jsonl`

Purpose: chunks representing candidate acts, table rows, or route entries.

JSONL schema:

```json
{
  "chunk_id": "PP_RETURN_ACTS_1844_47_p030_row012",
  "source_doc_id": "PP_RETURN_ACTS_1844_47",
  "page_start": 30,
  "page_end": 30,
  "line_start": 120,
  "line_end": 128,
  "raw_text": "...",
  "segmentation_method": "rule_v1",
  "segmentation_confidence": 0.85
}
```

---

### 6.4 `acts.csv`

Purpose: one row per Act / bill / Parliamentary authorisation unit.

Required columns:

```text
act_id
act_year
session_year
act_title_raw
act_title_clean
railway_company_raw
railway_company_clean
act_type
royal_assent_date
source_doc_id
source_page_start
source_page_end
source_line_start
source_line_end
raw_text_excerpt
extractor_model
prompt_version
extraction_run_id
extraction_confidence
manual_check
notes
```

Suggested `act_type` vocabulary:

```text
new_company
new_line
branch
extension
deviation
amendment
amalgamation
lease
purchase
capital_increase
abandonment
unknown
```

---

### 6.5 `authorized_segments.csv`

Purpose: one row per authorised route, branch, extension, deviation, or build-relevant segment.

This is the most important authorisation table.

Required columns:

```text
authorized_segment_id
act_id
act_year
session_year
company_name_raw
company_name_clean
segment_name_raw
segment_name_clean
route_start_raw
route_start_clean
route_end_raw
route_end_clean
intermediate_places_raw
intermediate_places_clean
counties_raw
counties_clean
authorized_miles
authorized_chains
authorized_length_miles_decimal
authorized_share_capital
authorized_loan_power
total_authorized_capital
capital_per_mile
segment_type
is_new_line
is_branch
is_extension
is_deviation
is_capital_only
is_amalgamation_or_lease
is_eligible_for_construction_rate
source_doc_id
source_page_start
source_page_end
source_line_start
source_line_end
raw_text_excerpt
extractor_model
prompt_version
extraction_run_id
extraction_confidence
manual_check
notes
```

Suggested `segment_type` vocabulary:

```text
new_line
branch
extension
deviation
capital_only
amalgamation_or_lease
abandonment
unknown
```

Important denominator rule:

- Use `is_eligible_for_construction_rate = True` for actual route-building items: new lines, branches, extensions, and possibly deviations if they involve measurable construction.
- Exclude pure capital increases, mergers, leases, name changes, and administrative amendments from the construction-rate denominator unless explicitly justified.

---

### 6.6 `annual_authorizations.csv`

Purpose: annual aggregate table generated from `authorized_segments.csv` and compared to benchmarks.

Required columns:

```text
year
authorized_miles_total
eligible_authorized_miles
authorized_capital_total
number_of_acts
number_of_segments
average_capital_per_mile
median_capital_per_mile
new_line_miles
branch_miles
extension_miles
capital_only_acts
benchmark_authorized_miles
difference_from_benchmark
percent_difference_from_benchmark
validation_status
notes
```

---

### 6.7 `lines.csv`

Purpose: one row per constructed/opened railway line from CAMPOP GIS or equivalent source.

Required columns:

```text
line_id
company_name_raw
company_name_clean
line_name_raw
line_name_clean
route_start_raw
route_start_clean
route_end_raw
route_end_clean
intermediate_places
opening_year
opening_date
line_length_miles
geometry_id
geometry_path
country
counties
source
notes
```

---

### 6.8 `line_segments.csv`

Purpose: smaller GIS segments suitable for matching to authorised route segments.

Required columns:

```text
gis_segment_id
line_id
company_name_clean
segment_start
segment_end
opening_year
segment_length_miles
geometry_path
county
nearest_towns
notes
```

If CAMPOP GIS already provides segment-level data, preserve its native segment IDs.

---

### 6.9 `match_candidates.csv`

Purpose: candidate matches from authorised segments to constructed GIS segments.

Required columns:

```text
candidate_id
authorized_segment_id
gis_segment_id
act_year
opening_year
company_score
route_start_score
route_end_score
intermediate_place_score
county_score
length_similarity_score
year_score
overall_score
candidate_rank
auto_match_candidate
notes
```

---

### 6.10 `matches.csv`

Purpose: final authorisation-to-construction match table.

Required columns:

```text
match_id
authorized_segment_id
matched_gis_segment_id
match_status
match_method
match_confidence
act_year
opening_year
opening_lag
authorized_miles
matched_built_miles
matched_length_ratio
built_by_1851
built_by_1852
built_by_1861
not_built_dummy
partial_match_dummy
decision_reason
reviewer
review_status
notes
```

Allowed `match_status`:

```text
matched
partial_matched
not_found
ambiguous
not_applicable
```

Allowed `match_method`:

```text
exact_name
fuzzy_name
route_place_match
county_length_match
llm_adjudicated
manual
not_applicable
```

---

### 6.11 `cohort_summary.csv`

Purpose: final table for the paper’s main result.

Required columns:

```text
act_year
authorized_miles_total
eligible_authorized_miles
authorized_capital_total
number_of_acts
number_of_segments
built_by_1851_miles
built_by_1852_miles
built_by_1861_miles
not_built_miles
construction_rate_1851
construction_rate_1852
construction_rate_1861
capital_weighted_construction_rate_1851
capital_weighted_construction_rate_1852
average_opening_lag
median_opening_lag
average_capital_per_mile
median_capital_per_mile
new_line_share
branch_share
extension_share
deviation_share
ambiguous_match_share
notes
```

Key formula:

```text
ConstructionRate_y = BuiltMiles_y / EligibleAuthorizedMiles_y
```

Capital-weighted formula:

```text
CapitalWeightedConstructionRate_y
= sum(AuthorizedCapital_i * Built_i) / sum(AuthorizedCapital_i)
```

---

## 7. Benchmarks

Create `config/benchmarks.yaml`.

Initial benchmark values, treated as approximate and source-dependent:

```yaml
authorized_miles:
  1843:
    odlyzko: 91
  1844:
    odlyzko: 805
  1845:
    odlyzko: 2700
    note: "May differ slightly depending on inclusion/exclusion of branches, amendments, and country coverage."
  1846:
    odlyzko: 4538
    note: "Some sources may report a slightly different total. Do not hard-fail without manual review."
  1847:
    odlyzko: 1354
  1850:
    odlyzko: 8
```

Validation rule:

- Compare generated annual totals to benchmarks.
- If difference exceeds configurable tolerance, write a validation warning.
- Do not silently alter data to match benchmarks.
- Always keep a `notes` field describing definition differences.

Suggested tolerance:

```yaml
tolerance_percent: 3.0
```

For exact Parliamentary Paper totals, add benchmark rows once source tables are confirmed.

---

## 8. LLM Use Policy

Use LLMs only for two tasks:

### Task 1: Structured extraction from messy OCR/table text

Input: segmented raw text.

Output: strict JSON matching the extraction schema.

LLM must include:

```text
evidence_text
confidence
source chunk id
```

### Task 2: Ambiguous match adjudication

Input: one authorised segment and top candidate GIS lines.

Output: match decision with reason.

LLM must not calculate aggregate statistics.

Arithmetic and aggregation must be done by Python only.

---

## 9. Extraction Prompt Template

Save as `config/prompts/extract_authorized_segment.md`.

```markdown
You are extracting structured data from a nineteenth-century British Parliamentary Paper about railway acts.

Return only valid JSON.
Do not infer values that are not present.
If a value is unclear, use null and explain in notes.
Preserve the raw company and route names exactly, and also provide cleaned versions if possible.

Required JSON schema:

{
  "act_title_raw": string | null,
  "company_name_raw": string | null,
  "act_year": integer | null,
  "session_year": integer | null,
  "route_start_raw": string | null,
  "route_end_raw": string | null,
  "intermediate_places_raw": [string],
  "counties_raw": [string],
  "authorized_miles": number | null,
  "authorized_chains": number | null,
  "authorized_capital_pounds": number | null,
  "loan_power_pounds": number | null,
  "segment_type": "new_line" | "branch" | "extension" | "deviation" | "capital_only" | "amalgamation_or_lease" | "abandonment" | "unknown",
  "is_eligible_for_construction_rate": boolean,
  "evidence_text": string,
  "notes": string,
  "confidence": number
}

Source metadata:
- source_doc_id: {{source_doc_id}}
- chunk_id: {{chunk_id}}
- page_start: {{page_start}}
- page_end: {{page_end}}
- line_start: {{line_start}}
- line_end: {{line_end}}

Raw text:
{{raw_text}}
```

---

## 10. Matching Prompt Template

Save as `config/prompts/adjudicate_match.md`.

```markdown
You are adjudicating whether a Parliamentary railway authorisation corresponds to a constructed/opened railway line in GIS data.

Return only valid JSON.
Base your decision on company name, route endpoints, intermediate places, counties, authorised length, GIS length, act year, and opening year.
Do not assume a match solely from company name.

Required JSON schema:

{
  "decision": "matched" | "partial_matched" | "not_found" | "ambiguous" | "not_applicable",
  "best_gis_segment_id": string | null,
  "match_confidence": number,
  "reason": string,
  "key_evidence": [string],
  "needs_manual_review": boolean
}

Authorised segment:
{{authorized_segment_json}}

Candidate GIS segments:
{{candidate_segments_json}}
```

---

## 11. Normalisation Rules

### 11.1 Length

```text
1 mile = 80 chains
length_decimal = miles + chains / 80
```

If only miles are present, chains = 0.

### 11.2 Capital

Convert all capital values to integer pounds.

Examples:

```text
£1,250,000 → 1250000
L.1,250,000 → 1250000
1,250,000l. → 1250000
```

### 11.3 Names

Maintain both raw and cleaned names.

```text
company_name_raw
company_name_clean
```

Do not overwrite raw names.

Create alias files if needed:

```text
data/processed/company_aliases.csv
data/processed/place_aliases.csv
```

### 11.4 Peak Bubble Cohort

In the final analysis table:

```text
peak_bubble_cohort = 1 if act_year in [1845, 1846]
peak_bubble_cohort = 0 if act_year in [1844, 1847]
```

Keep this configurable.

---

## 12. Matching Logic

Do not rely on company name alone.

Candidate scoring should use:

```text
company_name_similarity
route_start_similarity
route_end_similarity
intermediate_place_overlap
county_overlap
length_similarity
opening_year_condition
known_alias_bonus
```

Suggested scoring logic:

```text
overall_score =
  0.25 * company_score +
  0.25 * endpoint_score +
  0.15 * intermediate_place_score +
  0.15 * county_score +
  0.10 * length_score +
  0.10 * year_score
```

Auto-match only if:

```text
overall_score >= 0.90
opening_year >= act_year
length difference is reasonable
no conflicting top candidate
```

Send to adjudication if:

```text
0.65 <= overall_score < 0.90
or multiple candidates have close scores
or company name changed through amalgamation/lease
```

Mark `not_found` if:

```text
no candidate has plausible company/place/year similarity
```

Always preserve matching reasons.

---

## 13. Validation Gates

### Gate A: Schema Validation

Fail or warn on:

```text
missing act_year
missing company_name for build-relevant rows
non-numeric authorised miles
non-numeric capital when capital appears in raw text
invalid segment_type
missing source provenance
```

### Gate B: Logic Validation

Warn on:

```text
capital_per_mile <= 0 for build-relevant rows with capital
capital_per_mile extremely high or low
opening_year < act_year
matched_length_ratio > 1.5 or < 0.5
same source row extracted multiple times
same authorised segment matched to multiple unrelated GIS segments
```

### Gate C: Benchmark Validation

For each year:

```text
computed_authorized_miles vs benchmark_authorized_miles
computed_number_of_acts vs benchmark_number_of_acts if available
computed_authorized_capital vs benchmark_capital if available
```

Write report to:

```text
logs/validation_reports/validation_YYYYMMDD_HHMM.json
```

---

## 14. Main Analysis Outputs

Generate the following tables.

### 14.1 `outputs/tables/cohort_summary.csv`

Main result table.

### 14.2 `outputs/tables/peak_vs_nonpeak.csv`

Compare 1845–1846 vs 1844/1847.

Columns:

```text
cohort_group
authorized_miles
built_by_1851_miles
built_by_1852_miles
construction_rate_1851
construction_rate_1852
average_opening_lag
capital_weighted_construction_rate_1851
capital_weighted_construction_rate_1852
```

### 14.3 `outputs/tables/segment_type_summary.csv`

Construction rate by segment type.

Columns:

```text
segment_type
authorized_miles
built_by_1851_miles
construction_rate_1851
average_capital_per_mile
```

---

## 15. Figures to Generate

Create publication-ready PNG and SVG versions.

### Figure 1 — Timeline

```text
x-axis: year
series:
- railway stock index
- authorised miles
- railway investment
```

Use separate panels if scales differ too much.

### Figure 2 — Annual Authorisations

```text
x-axis: act_year
bar 1: authorised miles
bar 2: authorised capital
```

### Figure 3 — Cohort Construction Rate

```text
x-axis: act_year
y-axis: construction_rate_1851 / construction_rate_1852
```

### Figure 4 — Built vs Not Built Miles

```text
x-axis: act_year
stacked bars:
- built_by_1851_miles
- not_built_miles
```

### Figure 5 — Segment Type Realisation

```text
x-axis: segment_type
y-axis: construction_rate_1851
```

---

## 16. Command-Line Interface

Each script should be runnable independently.

Example commands:

```bash
python src/01_prepare_text.py \
  --manifest data/sources_manifest.csv \
  --out data/interim/page_text.jsonl

python src/02_segment.py \
  --input data/interim/page_text.jsonl \
  --out data/interim/segments_raw.jsonl

python src/03_extract.py \
  --input data/interim/segments_raw.jsonl \
  --out data/interim/authorized_segments_extracted.jsonl \
  --prompt config/prompts/extract_authorized_segment.md

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

python src/08_adjudicate.py \
  --candidates data/interim/match_candidates.csv \
  --authorized data/processed/authorized_segments.csv \
  --gis data/processed/line_segments.csv \
  --out data/processed/matches.csv

python src/09_aggregate.py \
  --authorized data/processed/authorized_segments.csv \
  --matches data/processed/matches.csv \
  --out data/processed/cohort_summary.csv

python src/10_plot.py \
  --cohort data/processed/cohort_summary.csv \
  --out outputs/figures/
```

---

## 17. Testing Plan

Create manually coded gold data before full extraction.

### Gold Sample

File:

```text
tests/gold/manually_coded_sample.csv
```

Recommended size:

```text
20–30 authorisation rows from 1846 first.
Then 20–30 from 1845.
```

Gold sample should include:

```text
company_name
route_start
route_end
authorized_miles
authorized_capital
segment_type
source_page
```

### Unit Tests

Test:

```text
length conversion
capital conversion
company name normalisation
place name normalisation
schema validation
benchmark difference calculation
fuzzy matching scoring
```

---

## 18. Acceptance Criteria

The pipeline is acceptable when:

1. Raw files are preserved and tracked in `sources_manifest.csv`.
2. Every extracted authorisation row has source provenance.
3. `authorized_segments.csv` passes schema validation.
4. Annual authorised miles are compared to benchmarks and validation reports are produced.
5. CAMPOP GIS is converted to `lines.csv` and `line_segments.csv`.
6. `matches.csv` records match method, confidence, and decision reason.
7. `cohort_summary.csv` computes construction rates by act year.
8. Ambiguous matches are flagged, not silently decided.
9. Figures can be regenerated from processed data.
10. The project can run on MVP years 1845–1846 before expanding.

---

## 19. Research Interpretation Guardrails

Use precise language.

Preferred:

```text
authorisation → construction/opening realisation
```

Avoid claiming route-level investment unless actual capital expenditure data exists.

Clarify distinction:

```text
Parliamentary authorisation = legal approval and planned capital/length.
Railway investment = actual money spent, usually available as aggregate annual data.
Construction/opening = actual line existed or opened in GIS/opening-year data.
```

The main empirical measure is not investment conversion, but construction/opening realisation.

---

## 20. Next Implementation Step

Start with the smallest useful unit.

1. Create scaffold.
2. Place one Parliamentary Paper TXT or OCR file under `data/raw/`.
3. Build `sources_manifest.csv`.
4. Segment 1846 sample pages.
5. Manually code 20–30 rows as gold sample.
6. Run LLM extraction on the same sample.
7. Compare extraction to gold sample.
8. Adjust schema and prompts.
9. Only then run full 1845–1846 extraction.

Do not attempt full 10-year extraction before the MVP validates successfully.
