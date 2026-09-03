"""Source catalogue matching (query) and fetch dispatcher."""
import pytest

from tobacco_gateway import fetch, query


def test_query_prefers_munich_sources():
    ids = [r.source_id for r in query("smoking prevalence Munich")]
    assert ids[0].startswith("muenchen")


def test_query_finds_open_data_sources():
    ids = [r.source_id for r in query("Rauchen Lungenkrebs Bundesland")]
    assert "rki_gbe_ncd" in ids


def test_unknown_source_raises():
    with pytest.raises(ValueError):
        fetch("does_not_exist")
