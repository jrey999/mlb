from sqlalchemy import create_engine, Column, Integer, REAL, Numeric, String, DateTime, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from data.funcs import iso_to_dt, get_team_id



engine = create_engine("sqlite:///db.sqlite3")
Base = declarative_base()
class Game(Base):

    __tablename__ = "game"
    
    game_id = Column(Integer, primary_key=True)
    game_date = Column(DateTime)
    away = Column(Integer)
    home = Column(Integer)
    status = Column(String)
    venue_id = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint("game_id"),
        ForeignKeyConstraint(["venue_id"], ["venue.venue_id"], ondelete="CASCADE", onupdate="NO ACTION")
    )

    def __init__(self, data: dict) -> None:

        self.game_id = data["gamePk"]
        self.game_date = iso_to_dt(data["gameDate"])
        self.away = data["teams"]["away"]["team"]["id"]
        self.home = data["teams"]["home"]["team"]["id"]
        self.status = data["status"]["abstractGameState"]
        self.venue_id = data["venue"]["id"]

class Inning(Base):

    __tablename__ = "inning"

    game_id = Column(Integer)
    team_id = Column(Integer)
    inning = Column(Integer)
    runs = Column(Integer)
    hits = Column(Integer)
    errors = Column(Integer)
    left_on_base = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint("game_id", "team_id", "inning"),
        ForeignKeyConstraint(["game_id"], ["game.game_id"], ondelete="CASCADE", onupdate="NO ACTION")
    )

    def __init__(self, inning: dict, side: str):

        self.game_id = inning["game_id"]
        self.team_id = inning[f"_{side}"]
        self.inning = inning["num"]
        self.runs = inning[side].get("runs")
        self.hits = inning[side]["hits"]
        self.errors = inning[side]["errors"]
        self.left_on_base = inning[side]["leftOnBase"]

class Pitch(Base):
    
    __tablename__ = "pitch"

    pitch_id = Column(String, primary_key=True)
    inning = Column(Integer)
    ab_number = Column(Integer)
    outs = Column(Integer)
    throws = Column(String)
    pitcher_id = Column(Integer)
    team_id = Column(Integer)
    result = Column(String)
    description = Column(String)
    strikes = Column(Integer)
    balls = Column(Integer)
    pre_strikes = Column(Integer)
    pre_balls = Column(Integer)
    call_name = Column(String)
    swinging_strike = Column(BOOLEAN)
    pitch_type = Column(String)
    start_speed = Column(REAL)
    extension = Column(REAL)
    zone = Column(Integer)
    spin_rate = Column(Integer)
    break_x = Column(Integer)
    break_z = Column(Integer)
    pitch_number = Column(Integer)
    player_total_pitches = Column(Integer)
    game_id = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint("pitch_id"),
        ForeignKeyConstraint(["game_id"], ["game.game_id"], ondelete="CASCADE", onupdate="NO ACTION")
    )

    def __init__(self, game_data: dict, game_id: int):
        
        self.pitch_id = game_data["play_id"]
        self.inning = game_data["inning"]
        self.ab_number = game_data["ab_number"]
        self.outs = game_data["outs"]
        self.throws = game_data["p_throws"]
        self.pitcher_id = game_data["pitcher"]
        self.team_id = game_data["team_batting_id"]
        self.result = game_data["result"]
        self.description = game_data["description"]
        self.strikes = game_data["strikes"]
        self.balls = game_data["balls"]
        self.pre_strikes = game_data["pre_strikes"]
        self.pre_balls = game_data["pre_balls"]
        self.call_name = game_data["call_name"]
        self.swinging_strike = game_data["is_strike_swinging"]
        self.pitch_type = game_data.get("pitch_type")
        self.start_speed = game_data.get("start_speed")
        self.extension = game_data.get("extension")
        self.zone = game_data.get("zone")
        self.spin_rate = game_data.get("spin_rate")
        self.break_x = game_data.get("breakX")
        self.break_z = game_data.get("breakZ")
        self.pitch_number = game_data["pitch_number"]
        self.player_total_pitches = game_data["player_total_pitches"]
        self.game_id = game_id

class Hit(Base):

    __tablename__ = "hit"

    pitch_id = Column(String, primary_key=True)
    team_id = Column(Integer)
    batter_id = Column(Integer)
    stance = Column(String)
    hit_speed = Column(Integer)
    hit_distance = Column(Integer)
    hit_angle = Column(Integer)
    is_barrell = Column(BOOLEAN)
    is_bip_out = Column(BOOLEAN)
    game_id = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint("pitch_id"),
        ForeignKeyConstraint(["game_id"], ["game.game_id"], ondelete="CASCADE", onupdate="NO ACTION")
    )

    def __init__(self, data: dict, game_id: int) -> None:

        self.pitch_id = data["play_id"]
        self.team_id = data["team_batting"]
        self.batter_id = data["batter"]
        self.stance = data["stand"]
        self.hit_speed = data.get("hit_speed")
        self.hit_distance = data.get("hit_distance")
        self.hit_angle = data.get("hit_angle")
        self.is_barrell = data.get("is_barrel")
        self.is_bip_out = data.get("is_bip_out")
        self.game_id = game_id

class Player(Base):

    __tablename__ = "player"

    player_id = Column(Integer)
    name = Column(String)
    team_id = Column(Integer)
    handed = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint("player_id"),
        ForeignKeyConstraint(["team_id"], ["team.team_id"], ondelete="CASCADE", onupdate="NO ACTION")
    )

    def __init__(self, data: dict, pitch_or_hit) -> None:

        self.player_id = data["pitcher"] if pitch_or_hit == "pitcher" else data["batter"]
        self.name = data["pitcher_name"] if pitch_or_hit == "pitcher" else data["batter_name"]
        self.team_id = get_team_id(data["team_fielding"]) if pitch_or_hit == "pitcher" else data["team_batting"]
        self.handed = data["p_throws"] if pitch_or_hit == "pitcher" else data["stand"]

class Team(Base):

    __tablename__ = "team"

    team_id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)

    def __init__(self, team_info: str) -> None:
        
        team_id, name, code = team_info.split("|")
        self.team_id = int(team_id)
        self.name = name
        self.code = code

class Venue(Base):

    __tablename__ = "venue"

    venue_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, venue_info: str) -> None:

        venue_id, name = venue_info.split("|")
        self.venue_id = int(venue_id)
        self.name = name

