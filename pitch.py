from data.datamodels import engine, Inning, Hit, Pitch, Player
from data.funcs import get_game_data, get_innings, get_pitcher_data
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


connection, Session, data = engine.connect(), sessionmaker(bind=engine), []
query = connection.execute(text(open("data/queries/recent_games.sql", "r").read().rstrip()))
games = [dict(zip(query.keys(), row)) for row in query.fetchall()]

for game in games:

    game_data = get_game_data(game)
    data += sum([[Inning(inning, "away"), Inning(inning, "home")] for inning in get_innings(game_data)], [])
    pitcher_data = get_pitcher_data(game_data)
    for _ in pitcher_data:

        data.append(Pitch(_, game["game_id"]))
        data.append(Hit(_, game["game_id"]))

        data.append(Player(_, "pitcher"))
        data.append(Player(_, "batter"))

with Session() as session:
    for _ in data:
        session.merge(_)
    session.commit()

session.close()