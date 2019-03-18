import sqlite3
import pandas as pd

#In memory db ':memory:; lives in RAM; useful for testing b/c fresh start each time
connection = sqlite3.connect('rankulator.db')
#connection = sqlite3.connect(':memory:')

c = connection.cursor()

# 3 quotes allow for multiline stuff
# Week(weekNum, team, numRush, succRush, numPass, succPass, succPct, numPlays, PPP)
c.execute("""CREATE TABLE stats (
             weekNum integer,
             teamName text,
             numRush integer,
             succRush integer,
             numPass integer,
             succPass integer,
             succPct real,
             numPlays integer,
             PointsPerPlay real
             )""")

#functions for application integration
def insert_team_data(csvfile):
    # Use connection as a context manager:
    # -This helps with rollback, setup, teardown, etc
    # -Makes it so a commit statement is not needed after every insert
    with connection:
        # Inserts data
        df = pd.read_csv(csvfile)
        df.to_sql('stats', connection, if_exists='append', index=False)

def get_team_by_name(team_name):
    # No Context manager b/c select doesn't need to be commited
    c.execute("SELECT * FROM stats WHERE teamName=:team", {'team': team_name})
    return c.fetchall()

# Hard coded
# c.execute("INSERT INTO stats VALUES ('TestTeam', 1, 2, 10, 1, 4, 5)")

# PlaceHolders (Option 1 is quicker but more vague. 2 is more wordy but well documented b/c use of dict)
# Can be used with select statement too.
# c.execute("INSERT INTO stats VALUES (?,?,?,?,?,?,?)", (tuple of values))
# c.execute("INSERT INTO stats VALUES (:teams, ..., :rushing_yards)", ('teams': value, ..., 'rushing_yards': value))

#c.execute("SELECT * FROM stats WHERE teams='Florida'")

# c.fetchone(), c.fetchmany(number of rows to fetch), c.fetchall()
# use after each select statement to use selected data (I think)
#print(c.fetchone())

#finishes transaction
#connection.commit()

#insert_team_data('testCombine.csv')
insert_team_data('test.csv')

c.execute("""CREATE TABLE team (
             name text,
             AVGsuccPct real,
             AVG_PPP real,
             Score real
             )""")

c.execute("""INSERT INTO team
             SELECT teamName, avg(succPCT), avg(PointsPerPlay), (avg(succPCT)+(100*avg(PointsPerPlay)))
             FROM stats
             GROUP BY teamName;
            """)

out = c.fetchall()


#out = get_team_by_name('Florida')
print(out)

connection.close()

# This may be useful later
#df = pandas.read_csv(csvfile)
#df.to_sql(table_name, conn, if_exists='append', index=False)

#Possibly create a trigger to insert data into team when stats is updated/inserted into
