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