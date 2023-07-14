SELECT
    game.game_id, inning.team_id, MAX(inning.inning),
    SUM(inning.runs), SUM(inning.hits), SUM(inning.errors),
    SUM(inning.left_on_base)
FROM
    inning
JOIN
    game
        ON
    inning.game_id = game.game_id
GROUP BY
    game.game_id, inning.team_id
ORDER BY
    game.game_date;
