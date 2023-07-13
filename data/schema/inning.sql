CREATE TABLE IF NOT EXISTS
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
        );