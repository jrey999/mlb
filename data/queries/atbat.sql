WITH last_pitch AS (
    SELECT
        x.pitch_id
    FROM
        (
            SELECT
                MAX(pitch.pitch_id) AS pitch_id, pitch.game_id, pitch.team_id, pitch.inning, pitch.ab_number
            FROM
                pitch
            JOIN
                hit ON pitch.pitch_id = hit.pitch_id
            JOIN
                game ON game.game_id = pitch.game_id
            GROUP BY
                pitch.game_id, pitch.team_id, pitch.inning, pitch.ab_number
            ORDER BY
                game.game_date, pitch.inning, pitch.ab_number
        ) AS x
)
SELECT
    pitch.team_id, pitch.pitcher_id, hit.team_id, hit.batter_id, pitch.throws,
    hit.stance, pitch.outs, pitch.balls, pitch.strikes, pitch.swinging_strike,
    pitch.pitch_type,  pitch.zone, pitch.spin_rate, pitch.break_x, pitch.break_z,
    pitch.player_total_pitches, hit.hit_speed, hit.hit_distance, hit.hit_angle, hit.is_barrell,
    hit.is_bip_out, pitch.result, pitch.game_id
FROM
    pitch
JOIN
    hit
        ON
    pitch.pitch_id = hit.pitch_id
JOIN
    game
        ON
    game.game_id = pitch.game_id
WHERE
    pitch.pitch_id IN last_pitch
ORDER BY
    game.game_date, pitch.inning, pitch.ab_number;
