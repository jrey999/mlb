CREATE TABLE IF NOT EXISTS
    team
        (
            team_id smallint NOT null,
            name text NOT null,
            code VARCHAR(4) NOT null,
                UNIQUE(code),
                PRIMARY KEY(team_id)
        );