import requests, json, sqlite3
import datetime as dt
from pytz import timezone as tz


DB = sqlite3.connect("db.sqlite3")
def get_date(days: int=None):

    return str(dt.date.today() + dt.timedelta(days=days if days else 0))

def get_schedule(schedule_url: str) -> dict:
    """makes the request for game table"""
    return requests.get(schedule_url).json()

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

class Pitches:
    
    def __init__(self, game_info: tuple[int, int, int]):
        
        self.game_id, self.away, self.home = game_info
        self.response = requests.get("https://baseballsavant.mlb.com/gf?game_pk={}".format(self.game_id)).json()
        self.home_pitchers = [key for key in self.response["home_pitchers"].keys()]
        self.away_pitchers = [key for key in self.response["away_pitchers"].keys()]
    
    @property
    def innings(self) -> list[tuple[int]]:

        return [
            (
                self.game_id, #game_id
                self.away, #away
                _["num"], #inning
                _["away"].get("runs"), #runs
                _["away"]["hits"], #hits
                _["away"]["errors"], #errors
                _["away"]["leftOnBase"], #left_on_base
                False if _["away"].get("runs") is None else True
            )
            for _ in self.response["scoreboard"]["linescore"]["innings"]
        ] + [
            (
                self.game_id, #game_id
                self.home, #home
                _["num"], #inning
                _["home"].get("runs"), #runs
                _["home"]["hits"], #hits
                _["home"]["errors"], #errors
                _["home"]["leftOnBase"], #left_on_base
                False if _["home"].get("runs") is None else True
            )
            for _ in self.response["scoreboard"]["linescore"]["innings"]
        ]
    @property
    def home_pitches(self) -> list:
        """returns all home pitchers pitch data"""
        return sum([
            [
            fmt_pitch(pitch, self.game_id) for pitch in self.response["home_pitchers"][home_pitcher]
            ]
            for home_pitcher in self.home_pitchers
        ], [])
    
    @property
    def away_pitches(self) -> list:
        """returns all away pitchers pitch data"""
        return sum([
            [
            fmt_pitch(pitch, self.game_id) for pitch in self.response["away_pitchers"][away_pitcher]
            ]
            for away_pitcher in self.away_pitchers
        ], [])
    
    @property
    def pitches(self) -> list:
        """returns a sorted list of tuples for each pitch data"""
        return sorted(self.away_pitches + self.home_pitches, key=lambda _: (_["pitch"][1], _["pitch"][2], _["pitch"][-3]))

class Schedule:

    def __init__(self, year: int):
        
        BASE="https://statsapi.mlb.com/api/v1/schedule"
        DATE="?sportId=1&startDate={}-03-01&endDate={}-11-01&".format(year, year)
        FIELDS="gameType=R&fields=dates,date,games,gamePk,status,abstractGameState,teams,away,home,team,id,name,gameDate,venue"
        self.response = requests.get(BASE+DATE+FIELDS).json()
        self.schedule = sum([date['games'] for date in self.response['dates']], [])

    @property
    def teams(self):

        return [
            _ for _ in dict(sorted({
                game["teams"]["away"]["team"]["id"]: {
                    "team_id": game["teams"]["away"]["team"]["id"],
                    "name": game["teams"]["away"]["team"]["name"],
                    "code": get_team(game["teams"]["away"]["team"]["name"])
                } for game in self.schedule
            }.items())).values()
        ]

    @property
    def game(self) -> list:

        return sorted(
            [
                (
                    game["gamePk"],
                    iso_to_dt(game["gameDate"]),
                    game["teams"]["away"]["team"]["id"],
                    game["teams"]["home"]["team"]["id"],
                    game["status"]["abstractGameState"],
                    game["venue"]["id"]
                ) for game in self.schedule
            ],
            key=lambda tuple: tuple[1]
            )
    
    @property
    def venues(self) -> list:

        return [
            (
                game["venue"]["id"], #venue_id
                game["venue"]["name"] #name
            )
            for game in self.schedule
        ]