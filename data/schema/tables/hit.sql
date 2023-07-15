CREATE TABLE IF NOT EXISTS
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
        );