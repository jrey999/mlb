CREATE TABLE IF NOT EXISTS
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
        );