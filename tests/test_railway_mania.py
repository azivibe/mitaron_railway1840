from src.railway_mania import clean_name, construction_rate, length_to_decimal, parse_pounds, score_candidate


def test_length_to_decimal():
    assert length_to_decimal(10, 40) == 10.5


def test_parse_pounds():
    assert parse_pounds("£1,250,000") == 1250000
    assert parse_pounds("1,250,000l.") == 1250000


def test_clean_name():
    assert clean_name("The London & York Railway Company") == "london and york"


def test_candidate_scoring_prefers_plausible_route():
    auth = {"company_name_raw": "London and York Railway", "route_start_raw": "London", "route_end_raw": "York", "authorized_miles": 190, "act_year": 1846}
    gis = {"company_name_raw": "London & York Railway Company", "segment_start": "London", "segment_end": "York", "segment_length_miles": 192, "opening_year": 1850}
    assert score_candidate(auth, gis).overall_score > 0.65


def test_construction_rate():
    assert construction_rate(25, 100) == 0.25
