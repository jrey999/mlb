from data.datamodels import Pitches, DB


cursor = DB.cursor()
cursor.execute(
    """
    SELECT
        game_id, away, home
    FROM
        game
    WHERE
        status = 'Final'
            AND
        (
            game_date > CURRENT_TIMESTAMP - interval '28 hour'
                OR
            game_id NOT IN (SELECT DISTINCT game_id FROM pitch)
        )
    ORDER BY
        game_date;
    """
)
game_ids = cursor.fetchall()
for game_id in game_ids:

    print("game_id: {}\n".format(game_id[0]))
    pitches = Pitches(game_id)
    cursor.executemany(
        """
        INSERT INTO
            inning
        (
            game_id, team_id, inning, runs,
            hits, errors, left_on_base, played
        )
            VALUES
        (
          %s, %s, %s, %s,
          %s, %s, %s, %s
        )
            ON CONFLICT(game_id, team_id, inning)
            DO UPDATE SET
        runs = EXCLUDED.runs,
        hits = EXCLUDED.hits,
        errors = EXCLUDED.errors,
        left_on_base = EXCLUDED.left_on_base,
        played = EXCLUDED.played;
        """,
        pitches.innings
    )
    pitches = pitches.pitches
    cursor.executemany(
        """
        INSERT INTO
            player
        (
            player_id, name, team_id, handed
        )
            VALUES
        (
            %s, %s, %s, %s
        )
            ON CONFLICT(player_id)
            DO UPDATE SET
        name = EXCLUDED.name,
        team_id = EXCLUDED.team_id,
        handed = EXCLUDED.handed;
        """,
        [player for player in set(sum([pitch["player"] for pitch in pitches], []))]
    )
        
    cursor.executemany(
        """
        INSERT INTO
            hit
        (
            pitch_id, team_id, batter_id,
            stance, hit_speed, hit_distance,
            hit_angle, is_barrell, is_bip_out,
            game_id
        )
            VALUES
        (
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s
        )
            ON CONFLICT(pitch_id)
            DO UPDATE SET
        stance = EXCLUDED.stance,
        hit_speed = EXCLUDED.hit_speed,
        hit_distance = EXCLUDED.hit_distance,
        hit_angle = EXCLUDED.hit_angle,
        is_barrell = EXCLUDED.is_barrell,
        is_bip_out = EXCLUDED.is_bip_out;
        """,
        [pitch["hit"] for pitch in pitches]
    )

    cursor.executemany(
        """
        INSERT INTO pitch
            (
                pitch_id, inning, ab_number, outs, throws,
                pitcher_id, team_id, result, description,
                strikes, balls, pre_strikes, pre_balls,
                call_name, swinging_strike, pitch_type,
                start_speed, extension, zone, spin_rate,
                break_x, break_z, pitch_number, player_total_pitches,
                game_id
            )
        VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        ON CONFLICT(pitch_id)
            DO
        UPDATE SET
            inning = EXCLUDED.inning,
            ab_number = EXCLUDED.ab_number,
            outs = EXCLUDED.outs,
            throws = EXCLUDED.throws,
            pitcher_id = EXCLUDED.pitcher_id,
            team_id = EXCLUDED.team_id,
            result = EXCLUDED.result,
            description = EXCLUDED.description,
            strikes = EXCLUDED.strikes,
            balls = EXCLUDED.balls,
            pre_strikes = EXCLUDED.pre_strikes,
            pre_balls = EXCLUDED.pre_balls,
            call_name = EXCLUDED.call_name,
            swinging_strike = EXCLUDED.swinging_strike,
            pitch_type = EXCLUDED.pitch_type,
            start_speed = EXCLUDED.start_speed,
            extension = EXCLUDED.extension,
            zone = EXCLUDED.zone,
            spin_rate = EXCLUDED.spin_rate,
            break_x = EXCLUDED.break_z,
            break_z = EXCLUDED.break_z,
            pitch_number = EXCLUDED.pitch_number,
            player_total_pitches = EXCLUDED.player_total_pitches;
        """,
        [pitch["pitch"] for pitch in pitches]
        )

    DB.commit()
