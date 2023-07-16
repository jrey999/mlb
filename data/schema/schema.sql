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
);CREATE TABLE IF NOT EXISTS
    game
        (
            game_id integer NOT null,
            game_date timestamptz NOT null,
            away tinyint NOT null,
            home tinyint NOT null,
            status text NOT null,
            venue_id integer NOT null,
                PRIMARY KEY(game_id),
                FOREIGN KEY(venue_id) REFERENCES venue(venue_id)
                ON DELETE CASCADE ON UPDATE NO ACTION
        );CREATE TABLE IF NOT EXISTS
    hit
        (
            pitch_id text NOT null,
            team_id smallint NOT null,
            batter_id bigint NOT null,
            stance VARCHAR(7),
            hit_speed integer,
            hit_distance integer,
            hit_angle integer,
            is_barrell bool,
            is_bip_out bool,
            game_id integer NOT null,
                PRIMARY KEY(pitch_id),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );CREATE TABLE IF NOT EXISTS
    inning
        (
            game_id integer NOT null,
            team_id integer NOT null,
            inning smallint NOT null,
            runs tinyint,
            hits tinyint,
            errors tinyint,
            left_on_base tinyint,
            played integer NOT null,
                PRIMARY KEY(game_id, team_id, inning),
                    FOREIGN KEY(team_id) REFERENCES team(team_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );CREATE TABLE IF NOT EXISTS
    money_line
        (
            game_id text NOT null,
            sportsbook text NOT null,
            team VARCHAR(3) NOT null,
            price real,
            updated timestamptz NOT null,
                PRIMARY KEY(game_id, sportsbook, team, price),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );CREATE TABLE IF NOT EXISTS
    odds
        (
            game_id text NOT null,
            away text NOT null,
            home text NOT null,
            game_date timestamptz NOT null,
                PRIMARY KEY(game_id)
        );CREATE TABLE IF NOT EXISTS
    pitch
        (
            pitch_id text NOT null,
            inning smallint NOT null,
            ab_number smallint NOT null,
            outs smallint NOT null,
            throws VARCHAR(7) NOT null,
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
            pitch_type VARCHAR(7),
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
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );CREATE TABLE IF NOT EXISTS
    player
        (
            player_id integer NOT null,
            name text NOT null,
            team_id smallint NOT null,
            handed VARCHAR(7),
                PRIMARY KEY(player_id),
                FOREIGN KEY(team_id) REFERENCES team(team_id)
                ON DELETE CASCADE ON UPDATE NO ACTION
        );CREATE TABLE IF NOT EXISTS
    season
        (
            season_id smallint PRIMARY KEY,
            season_start timestamptz,
            playoffs_start timestamptz,
            season_end timestamptz
        );CREATE TABLE IF NOT EXISTS
    spread
        (
            game_id text NOT null,
            sportsbook text NOT null,
            team VARCHAR(3) NOT null,
            price real,
            point numeric(4, 1),
            updated timestamptz NOT null,
                PRIMARY KEY(game_id, sportsbook, team, price, point),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );CREATE TABLE IF NOT EXISTS
    team
        (
            team_id smallint NOT null,
            name text NOT null,
            code VARCHAR(4) NOT null,
                UNIQUE(code),
                PRIMARY KEY(team_id)
        );CREATE TABLE IF NOT EXISTS
    total
        (
            game_id text NOT null,
            sportsbook text NOT null,
            over_under VARCHAR(5) NOT null,
            price real,
            point numeric(4, 1),
            updated timestamptz NOT null,
                PRIMARY KEY(game_id, sportsbook, over_under, price, point),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );CREATE TABLE IF NOT EXISTS
    venue
        (
            venue_id integer NOT null,
            name text NOT null,
                PRIMARY KEY(venue_id)
        );