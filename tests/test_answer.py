"""Deterministic question engine (Python side)."""
import pytest

from tobacco_gateway import indicators as I


@pytest.fixture(scope="module")
def df():
    return I.load()


@pytest.mark.parametrize("question,indicator,geo,breakdown", [
    ("Wie viele Menschen rauchen in Bayern?", "smoking_current", "Bayern", None),
    ("Rauchen nach Bildung in Deutschland", "smoking_current", "Deutschland", "education"),
    ("Entwicklung des Rauchens in Deutschland seit 2003", "smoking_current", "Deutschland", "year"),
    ("Lungenkrebs-Sterblichkeit in Bayern im Zeitverlauf", "lung_cancer_mortality", "Bayern", "year"),
    ("Rauchen in München", "smoking_current", "München", None),
    ("Rauchen im Vergleich der Bundesländer", "smoking_current", "Deutschland", "geo_name"),
    ("Tabakkontrolle Deutschland", "tobacco_control_score", "Deutschland", None),
])
def test_parse(question, indicator, geo, breakdown):
    sel = I.parse_question(question)
    assert (sel.indicator, sel.geo, sel.breakdown) == (indicator, geo, breakdown)


def test_answers_contain_numbers_and_sources(df):
    a = I.answer("Wie viele Menschen rauchen in Bayern?", df)
    assert "20,5 %" in a.text and "26,4 %" in a.text
    assert set(a.sources) == {"destatis_mikrozensus", "rki_gbe_ncd"}


def test_no_data_is_stated_not_invented(df):
    a = I.answer("E-Zigaretten in Bayern", df)
    assert a.data.empty and "keine Werte" in a.text


def test_youth_fallback_to_bavarian_school_survey(df):
    a = I.answer("Rauchen bei Jugendlichen in Bayern", df)
    assert a.selection.indicator == "youth_smoking_30d" and "21,4 %" in a.text


def test_sex_filter(df):
    a = I.answer("Wie viele Frauen rauchen täglich in Bayern?", df)
    assert a.selection.sex == "weiblich" and a.selection.indicator == "smoking_daily"
    assert (a.data["sex"] == "weiblich").all()


def test_select_time_series_lower_bound(df):
    d = I.select(df, "lung_cancer_mortality", "Bayern", breakdown="year", year=2015)
    assert d["year"].min() == 2015 and d["year"].max() >= 2022
