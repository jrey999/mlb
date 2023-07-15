CREATE TABLE IF NOT EXISTS game (
  game_id integer NOT null,
  game_date timestamptz NOT null,
  away tinyint NOT null,
  home tinyint NOT null,
  status text NOT null,
  venue_id integer NOT null,
  PRIMARY KEY(game_id),
  FOREIGN KEY(venue_id) REFERENCES venue(venue_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS hit (
  pitch_id text NOT null,
  team_id smallint NOT null,
  batter_id bigint NOT null,
  stance varchar(7),
  hit_speed integer,
  hit_distance integer,
  hit_angle integer,
  is_barrell bool,
  is_bip_out bool,
  game_id integer NOT null,
  PRIMARY KEY(pitch_id),
  FOREIGN KEY(game_id) REFERENCES game(game_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS inning (
  game_id integer NOT null,
  team_id integer NOT null,
  inning smallint NOT null,
  runs tinyint NOT null,
  hits tinyint NOT null,
  errors tinyint NOT null,
  left_on_base tinyint NOT null,
  PRIMARY KEY(game_id, team_id, inning),
  FOREIGN KEY(team_id) REFERENCES team(team_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS pitch (
  pitch_id text NOT null,
  inning smallint NOT null,
  ab_number smallint NOT null,
  outs smallint NOT null,
  throws varchar(7) NOT null,
  pitcher_id integer NOT null,
  team_id smallint NOT null,
  result text,
  description text,
  strikes smallint NOT null,
  balls smallint NOT null,
  pre_strikes smallint,
  pre_balls smallint,
  call_name text,
  swinging_strike bool,
  pitch_type varchar(7),
  start_speed real,
  extension real,
  zone smallint,
  spin_rate integer,
  break_x smallint,
  break_z smallint,
  pitch_number smallint,
  player_total_pitches smallint,
  game_id integer NOT null,
  PRIMARY KEY(pitch_id),
  FOREIGN KEY(game_id) REFERENCES game(game_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS player (
  player_id integer NOT null,
  name text NOT null,
  team_id smallint NOT null,
  handed varchar(7),
  PRIMARY KEY(player_id),
  FOREIGN KEY(team_id) REFERENCES team(team_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS season (
  season_id smallint PRIMARY KEY,
  season_start timestamptz,
  playoffs_start timestamptz,
  season_end timestamptz
);

CREATE TABLE IF NOT EXISTS team (
  team_id smallint NOT null,
  name text NOT null,
  code varchar(4) NOT null,
  UNIQUE(code),
  PRIMARY KEY(team_id)
);

CREATE TABLE IF NOT EXISTS venue (
  venue_id integer NOT null,
  name text NOT null,
  PRIMARY KEY(venue_id)
);

CREATE TABLE IF NOT EXISTS
    box_score
(
    game_id integer NOT null,
    team_id integer NOT null,
    innings tinyint NOT null,
    runs tinyint NOT null,
    hits tinyint NOT null,
    errors tinyint NOT null,
    left_on_base tinyint NOT null,
        PRIMARY KEY(game_id, team_id),
            FOREIGN KEY(game_id) REFERENCES game(game_id)
            ON DELETE CASCADE ON UPDATE NO ACTION
            FOREIGN KEY(team_id) REFERENCES team(team_id)
            ON DELETE CASCADE ON UPDATE NO ACTION
);