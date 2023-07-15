import json, datetime
from data.datamodels import Schedule, DB


schedule, cursor, teamidmap = Schedule(datetime.datetime.now().year), DB.cursor(), {}
cursor.execute(open("data/schema/tables/season.sql", "r").read().rstrip())
cursor.execute(open("data/schema/tables/team.sql", "r").read().rstrip())
for team in schedule.teams:

    teamidmap[team["code"]] = team["team_id"]
    cursor.execute(
        """
        INSERT INTO
            team
        (
            team_id, name, code
        )
            VALUES
        (
            ?, ?, ?
        )
            ON CONFLICT(team_id)
            DO UPDATE SET
        name = ExCLUDED.name,
        code = ExCLUDED.code;
        """,
        tuple(team.values())
    )

for venue in schedule.venues:

    cursor.execute(
        """
        INSERT INTO
            venue
        (
            venue_id, name
        )
            VALUES
        (
            ?, ?
        )
            ON CONFLICT(venue_id)
            DO UPDATE SET
        name = EXCLUDED.name;
        """,
        venue
    )

DB.commit()
json.dump(teamidmap, open("meta/teamidmap.json", "w"), indent=0)
cursor.execute(open("data/schema/tables/game.sql", "r").read().rstrip())
for game in schedule.game:
    print("game_id:{}\n".format(game[0]))
    cursor.execute(
        """
        INSERT INTO
            game
        (
            game_id, game_date, away, home, status, venue_id
        )
            VALUES
        (
            ?, ?, ?, ?, ?, ?
        )
            ON CONFLICT(game_id)
            DO UPDATE SET
        game_date = EXCLUDED.game_date,
        away = ExCLUDED.away,
        home = ExCLUDED.home,
        status = ExCLUDED.status,
        venue_id = EXCLUDED.venue_id;
        """,
        game
    )
DB.commit()