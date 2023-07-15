CREATE TABLE IF NOT EXISTS
    player
        (
            player_id integer NOT null,
            name text NOT null,
            team_id smallint NOT null,
            handed VARCHAR(7),
                PRIMARY KEY(player_id),
                FOREIGN KEY(team_id) REFERENCES team(team_id)
                ON DELETE CASCADE ON UPDATE NO ACTION
        );