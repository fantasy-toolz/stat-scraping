import pandas as pd
import pytest

import mlbstatscraping as ss


@pytest.fixture
def sample_hitting_data():
    return pd.DataFrame(
        {
            "Name": ["Mookie Betts"],
            "Team": ["LAD"],
            "Season": [2024],
            "G": [116],
            "PA": [516],
            "HR": [19],
        }
    )


@pytest.fixture
def sample_pitching_data():
    return pd.DataFrame(
        {
            "Name": ["Tarik Skubal"],
            "Team": ["DET"],
            "season": [2024],
            "G": [31],
            "IP": [192.0],
            "SO": [228],
        }
    )


def test_get_fangraphs_data_hitting_calls_hitting_scraper(
    monkeypatch, sample_hitting_data
):
    calls = []

    def fake_hitting_scraper(years, daystart="", dayend=""):
        calls.append((years, daystart, dayend))
        return sample_hitting_data

    monkeypatch.setattr(ss.fgs, "grab_fangraphs_hitting_data", fake_hitting_scraper)

    result = ss.get_fangraphs_data(
        "hitting", ["2024"], daystart="2024-04-01", dayend="2024-05-01"
    )

    pd.testing.assert_frame_equal(result, sample_hitting_data)
    assert calls == [(["2024"], "2024-04-01", "2024-05-01")]


def test_get_fangraphs_data_pitching_calls_pitching_scraper(
    monkeypatch, sample_pitching_data
):
    calls = []

    def fake_pitching_scraper(years, daystart="", dayend=""):
        calls.append((years, daystart, dayend))
        return sample_pitching_data

    monkeypatch.setattr(ss.fgs, "grab_fangraphs_pitching_data", fake_pitching_scraper)

    result = ss.get_fangraphs_data("pitching", ["2024"])

    pd.testing.assert_frame_equal(result, sample_pitching_data)
    assert calls == [(["2024"], "", "")]


def test_invalid_stat_type_raises_error(monkeypatch):
    def scraper_should_not_be_called(*args, **kwargs):
        raise AssertionError("Fangraphs scraper should not be called")

    monkeypatch.setattr(
        ss.fgs, "grab_fangraphs_hitting_data", scraper_should_not_be_called
    )
    monkeypatch.setattr(
        ss.fgs, "grab_fangraphs_pitching_data", scraper_should_not_be_called
    )

    with pytest.raises(ValueError, match="Invalid playertype"):
        ss.get_fangraphs_data("invalid_type", ["2024"])


def test_daystart_year_must_match_requested_years(monkeypatch):
    def scraper_should_not_be_called(*args, **kwargs):
        raise AssertionError("Fangraphs scraper should not be called")

    monkeypatch.setattr(
        ss.fgs, "grab_fangraphs_hitting_data", scraper_should_not_be_called
    )

    with pytest.raises(ValueError, match=r"daystart year \(2023\)"):
        ss.get_fangraphs_data("hitting", ["2024"], daystart="2023-04-01")


def test_daystart_year_can_match_any_requested_year(monkeypatch, sample_hitting_data):
    calls = []

    def fake_hitting_scraper(years, daystart="", dayend=""):
        calls.append((years, daystart, dayend))
        return sample_hitting_data

    monkeypatch.setattr(ss.fgs, "grab_fangraphs_hitting_data", fake_hitting_scraper)

    result = ss.get_fangraphs_data(
        "hitting", ["2023", "2024"], daystart="2023-04-01"
    )

    pd.testing.assert_frame_equal(result, sample_hitting_data)
    assert calls == [(["2023", "2024"], "2023-04-01", "")]
