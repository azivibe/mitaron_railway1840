import importlib.util
from pathlib import Path

import pandas as pd

from src.railway_mania import (
    clean_name,
    construction_rate,
    eligible_for_construction_rate,
    length_to_decimal,
    parse_pounds,
    score_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "src" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_length_to_decimal():
    assert length_to_decimal(10, 40) == 10.5
    assert length_to_decimal("", "") is None


def test_parse_pounds():
    assert parse_pounds("£1,250,000") == 1250000
    assert parse_pounds("1,250,000l.") == 1250000


def test_eligible_for_construction_rate():
    assert eligible_for_construction_rate("new_line") is True
    assert eligible_for_construction_rate("branch") is True
    assert eligible_for_construction_rate("extension") is True
    assert eligible_for_construction_rate("capital_only") is False
    assert eligible_for_construction_rate("new_line", "false") is False


def test_clean_name():
    assert clean_name("The London & York Railway Company") == "london and york"


def test_score_candidate_prefers_plausible_route_and_rejects_pre_act_opening():
    auth = {"company_name_raw": "London and York Railway", "route_start_raw": "London", "route_end_raw": "York", "authorized_miles": 190, "act_year": 1846}
    gis = {"company_name_raw": "London & York Railway Company", "segment_start": "London", "segment_end": "York", "segment_length_miles": 192, "opening_year": 1850}
    assert score_candidate(auth, gis).overall_score > 0.65
    pre_act = {**gis, "opening_year": 1840}
    assert score_candidate(auth, pre_act).year_score == 0.0


def test_construction_rate():
    assert construction_rate(25, 100) == 0.25


def test_04_normalize_output_columns(tmp_path):
    normalize = load_script("04_normalize")
    acts = tmp_path / "acts.csv"
    segments = tmp_path / "authorized_segments.csv"

    normalize.main(FIXTURES / "authorized_segments_extracted.jsonl", acts, segments)

    df = pd.read_csv(segments)
    expected = {
        "authorized_segment_id",
        "act_id",
        "act_year",
        "company_name_clean",
        "route_start_clean",
        "route_end_clean",
        "authorized_length_miles_decimal",
        "total_authorized_capital",
        "is_eligible_for_construction_rate",
        "source_doc_id",
        "source_page",
        "source_line_start",
        "source_line_end",
        "raw_text_excerpt",
        "confidence",
    }
    assert expected.issubset(df.columns)
    assert len(df) == 5


def test_07_match_includes_opening_year_and_matched_built_miles(tmp_path):
    normalize = load_script("04_normalize")
    prepare_gis = load_script("06_prepare_gis")
    matcher = load_script("07_match")
    segments = tmp_path / "authorized_segments.csv"
    lines = tmp_path / "lines.csv"
    gis_segments = tmp_path / "line_segments.csv"
    candidates = tmp_path / "match_candidates.csv"
    matches = tmp_path / "matches.csv"

    normalize.main(FIXTURES / "authorized_segments_extracted.jsonl", tmp_path / "acts.csv", segments)
    prepare_gis.main(FIXTURES / "campop_gis_sample.csv", lines, gis_segments)
    matcher.main(segments, gis_segments, candidates, matches, auto_threshold=0.85)

    cand = pd.read_csv(candidates)
    match = pd.read_csv(matches)
    assert cand.groupby("authorized_segment_id").size().max() <= 5
    for col in ["opening_year", "matched_built_miles", "matched_length_ratio", "segment_length_miles", "line_length_miles"]:
        assert col in match.columns
    assert "AUTH_000005" not in set(match["authorized_segment_id"])
    assert (match["opening_year"] >= 1845).all()


def test_09_aggregate_produces_correct_construction_rates_from_fixtures(tmp_path):
    normalize = load_script("04_normalize")
    prepare_gis = load_script("06_prepare_gis")
    matcher = load_script("07_match")
    aggregate = load_script("09_aggregate")
    segments = tmp_path / "authorized_segments.csv"
    gis_segments = tmp_path / "line_segments.csv"
    matches = tmp_path / "matches.csv"
    out = tmp_path / "cohort_summary.csv"

    normalize.main(FIXTURES / "authorized_segments_extracted.jsonl", tmp_path / "acts.csv", segments)
    prepare_gis.main(FIXTURES / "campop_gis_sample.csv", tmp_path / "lines.csv", gis_segments)
    matcher.main(segments, gis_segments, tmp_path / "match_candidates.csv", matches, auto_threshold=0.85)
    aggregate.main(segments, matches, out)

    summary = pd.read_csv(out).set_index("act_year")
    assert summary.loc[1845, "eligible_authorized_miles"] == 40
    assert summary.loc[1845, "built_by_1851_miles"] == 30
    assert summary.loc[1845, "built_by_1852_miles"] == 40
    assert summary.loc[1845, "construction_rate_1851"] == 0.75
    assert summary.loc[1845, "construction_rate_1852"] == 1.0
    assert summary.loc[1846, "eligible_authorized_miles"] == 35
    assert summary.loc[1846, "built_by_1851_miles"] == 0
    assert summary.loc[1846, "built_by_1852_miles"] == 0
    assert summary.loc[1846, "construction_rate_1851"] == 0.0
    assert summary.loc[1846, "construction_rate_1852"] == 0.0
    assert summary.loc[1846, "number_of_segments"] == 3
    assert "number_matched_segments" in summary.columns
    assert "ambiguous_or_unmatched_segments" in summary.columns
