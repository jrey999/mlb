SELECT
        game_id, away, home
    FROM
        game
    WHERE
        status = 'Final'
            AND
        (
            game_date > datetime('now', '-28 hours')
                OR
            game_id NOT IN (SELECT DISTINCT game_id FROM pitch)
        )
    ORDER BY
        game_date;