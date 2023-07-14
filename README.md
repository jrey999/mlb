# mlb

Repository to create a sqlite DB of data from the mlb.stats API

# To create the database
create tables 
```bash
./shell/schema.sh
```

collect data for the team, venue and game tables
```bash
python game.py
```

collect data for the inning, player, hit and pitch tables
```bash
python pitch.py
```

schema can be changed by changing the SQL in the schema folder, ERD of the table is available below
![ERD](ERD.png)