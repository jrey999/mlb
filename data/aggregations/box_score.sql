INSERT INTO
    box_score
(
    game_id, team_id, innings, runs,
    hits, errors, left_on_base
)
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
WHERE
    game.game_id NOT IN (SELECT DISTINCT game_id FROM box_score)
GROUP BY
    game.game_id, inning.team_id
ORDER BY
    game.game_date

ON CONFLICT 
    (game_id, team_id)
DO UPDATE SET
innings = EXCLUDED.innings,
runs = EXCLUDED.runs,
hits = EXCLUDED.hits,
errors = EXCLUDED.errors,
left_on_base = EXCLUDED.left_on_base;