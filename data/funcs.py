import requests, json
import datetime as dt
from pytz import timezone as tz


def get_date(days: int=None):

    return str(dt.date.today() + dt.timedelta(days=days if days else 0))

TODAY = dt.datetime.today()
DATE="?sportId=1&startDate={}-03-01&endDate={}-12-01&".format(TODAY.year, TODAY.year)
def get_schedule() -> list[dict]:

    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule{DATE}gameType=R&fields=dates,date,games,gamePk,status,abstractGameState,teams,away,home,team,id,name,gameDate,venue"
    return sum([date['games'] for date in requests.get(schedule_url).json()['dates']], [])

def get_innings(game_data: dict) -> list[dict]:

    return [
        {
            **dict,
            **{"game_id": game_data["scoreboard"]["gamePk"], "_away": game_data["away"], "_home": game_data["home"]}
            } for dict in game_data["scoreboard"]["linescore"]["innings"]
        ]

def get_teams(schedule: list[dict]) -> set[str]:

    return {
        "{}|{}|{}".format(
            game["teams"]["away"]["team"]["id"],
            game["teams"]["away"]["team"]["name"],
            get_team(game["teams"]["away"]["team"]["name"])
            ) for game in schedule
    }

def get_venues(schedule: list[dict]) -> set[str]:

    return {
        "{}|{}".format(game["venue"]["id"], game["venue"]["name"]) for game in schedule
    }

def get_game_data(game_info: dict) -> dict:

    return {
        **requests.get("https://baseballsavant.mlb.com/gf?game_pk={}".format(game_info["game_id"])).json(),
        **{"away": game_info["away"], "home": game_info["home"]}
        }

def get_pitcher_data(game_data: dict) -> list[str]:

    return sum([value for value in game_data["home_pitchers"].values()] + [value for value in game_data["away_pitchers"].values()], [])

def tz_aware_today(time_zone: str):
    """takes in a timezone string and returns the timezone aware now time"""
    return tz(time_zone).localize(dt.datetime.today())

def utc_aware(datetime_object: dt.datetime):

    return tz("UTC").localize(datetime_object)

def iso_to_dt(iso_string: str) -> dt.datetime:
    """takes in an iso string and returns a datetime object"""
    date, time = iso_string.split("T")[0].split("-"), iso_string.split("T")[1].split("Z")[0].split(":")
    return utc_aware(dt.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[0]), int(time[1])))

def get_team(team_name: str) -> str:
    """takes in the spelled out team name and returns the 2 or letter team code"""
    return json.load(open("meta/teammap.json", "r")).get(team_name)

def get_team_id(team_code: str) -> int:

    return json.load(open("meta/teamidmap.json", "r")).get(team_code)

def fmt_is_barrel(is_barrel: int or None) -> bool or None:
    """formats the is_barrel field"""
    return bool(is_barrel) if is_barrel is not None else None

def fmt_is_bip_out(is_bip_out: str) -> bool:
    """formats the is_bip_out field"""
    return False if is_bip_out == "N" else True

def fmt_hit_(value: str or None) -> float or None:
    """formats the following fields; 'hit_speed','hit_distance' ,'hit_angle' """
    return float(value) if value is not None else None

def fmt_pitch(pitch: dict, game_id: int) -> dict[str:tuple, str:tuple]:
    """takes in a dict of pitch data and returns a tuple of formatted data"""
    return {
        "pitch": (
            pitch["play_id"], #play_id
            pitch["inning"], #inning
            pitch["ab_number"], #ab_number
            pitch["outs"], #outs
            pitch["p_throws"], #p_throws
            pitch["pitcher"], #pitcher_id
            get_team_id(pitch["team_fielding"]), #team_fielding
            pitch["result"], #result
            pitch["description"], #description
            pitch["strikes"], #strikes
            pitch["balls"], #balls
            pitch["pre_strikes"], #pre_strikes
            pitch["pre_balls"], #pre_balls
            pitch["call_name"], #call_name
            pitch["is_strike_swinging"], #strike_swinging
            pitch.get("pitch_type"), #pitch_type
            pitch.get("start_speed"), #start_speed
            pitch.get("extension"), #extension
            pitch.get("zone"), #zone
            pitch.get("spin_rate"), #spin_rate
            pitch.get("breakX"), #break_x,
            pitch.get("breakZ"), #break_z
            pitch["pitch_number"], #pitch_number
            pitch["player_total_pitches"], #player_total_pitches
            game_id #game_id
        ),
    "hit": (
            pitch["play_id"],
            get_team_id(pitch["team_batting"]), #team_batting
            pitch["batter"], #batter_id
            pitch["stand"], #stand
            fmt_hit_(pitch.get("hit_speed")), #hit_speed
            fmt_hit_(pitch.get("hit_distance")), #hit_distance
            fmt_hit_(pitch.get("hit_angle")), #hit_angle
            fmt_is_barrel(pitch.get("is_barrel")), #is_barrel
            fmt_is_bip_out(pitch["is_bip_out"]), #is_bip_out
            game_id #game_id
    ),
    "player": [
        (
            pitch["pitcher"], #pitcher_id
            pitch["pitcher_name"], #pitcher_name
            get_team_id(pitch["team_fielding"]), #team_fielding
            pitch["p_throws"], #p_throws
        ),
        (
            pitch["batter"], #batter_id
            pitch["batter_name"], #batter_name
            get_team_id(pitch["team_batting"]), #team_batting
            pitch["stand"], #stand
        )
    ]
    }