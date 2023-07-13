CREATE TABLE IF NOT EXISTS
    season
        (
            season_id smallint PRIMARY KEY,
            season_start timestamptz,
            playoffs_start timestamptz,
            season_end timestamptz
        );