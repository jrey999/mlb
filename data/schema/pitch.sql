CREATE TABLE IF NOT EXISTS
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
        );