from mlb.datamodels import get_date, get_team, get_team_id, fmt_pitch, Pitches
import datetime as dt
import json


def test_empty_get_date() -> None:

    assert get_date() == str(dt.date.today())

def test_negative_get_date() -> None:

    assert get_date(-5) == str(dt.date.today() - dt.timedelta(days=5))

def test_get_date() -> None:

    assert get_date(4) == str(dt.date.today() + dt.timedelta(days=4))

def test_get_team() -> None:

    assert get_team("Pittsburgh Pirates") == "PIT"

def test_get_team_id() -> None:

    assert get_team_id("KC") == 118

def test_fmt_pitch() -> None:

    assert fmt_pitch(json.load(open("tests/sampledata/pitch.json", "r")), 717507)["pitch"] == (
        "c83fc0c1-b6b8-4701-b093-0652d7e5d3b6", 7, 67, 2, "L", 622065, 113,
        "Lineout", "In play, out(s)", 2, 2, 2, 2, "In Play", False, "SI",
        91, 6.295532413672862, 6, 2360, 16, 28, 6, 8, 717507
    )

def test_fmt_pitch_hit() -> None:

    assert fmt_pitch(json.load(open("tests/sampledata/pitch.json", "r")), 717507)["hit"] == (
        "c83fc0c1-b6b8-4701-b093-0652d7e5d3b6", 120, 600869, "R", 100.7, 377,
        21, False, True, 717507
    )

def test_pitches_innings() -> None:

    for element in Pitches((717507, 113, 120)).innings:

        assert isinstance(element, tuple)