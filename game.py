from data.datamodels import Team, Venue, Game, engine
from data.funcs import get_schedule, get_teams, get_venues
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert


Session, data, schedule = sessionmaker(bind=engine), [], get_schedule()
data =  [Venue(venue) for venue in get_venues(schedule)] + [Game(_) for _ in schedule] + [Team(team) for team in get_teams(schedule)]

with Session() as session:
    for _ in data:
        session.merge(_)
    session.commit()

session.close()