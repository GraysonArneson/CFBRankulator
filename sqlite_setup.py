import sqlite3

#In memory db ':memory:''; lives in RAM; useful for testing b/c fresh start each time
connection = sqlite3.connect('rankulator.db')

c = connection.cursor()

#3 quotes allow for multiline stuff
# c.execute("""CREATE TABLE stats (
#             teams text, # I messed up and made it plural
#             successful_passes integer,
#             total_passes integer,
#             passing_yards integer,
#             successful_runs integer,
#             total_runs integer,
#             rushing_yards integer
#             )""")

#functions for application integration
def insert_team_data(obj):
    # Use connection as a context manager:
    # -This helps with rollback, setup, teardown, etc
    # -Makes it so a commit statement is not needed after every insert
    with connection:
        # Inserts data
        c.execute("INSERT INTO stats VALUES (:teams, ..., :rushing_yards)", ('teams': obj.value, ..., 'rushing_yards': obj.value))

def get_team_by_name(team_name):
    # No Context manager b/c select doesn't need to be commited
    c.execute("SELECT * FROM stats WHERE teams=:teams", {'teams': team_name})
    return c.fetchall()

# Hard coded
# c.execute("INSERT INTO stats VALUES ('TestTeam', 1, 2, 10, 1, 4, 5)")

# PlaceHolders (Option 1 is quicker but more vague. 2 is more wordy but well documented b/c use of dict)
# Can be used with select statement too.
# c.execute("INSERT INTO stats VALUES (?,?,?,?,?,?,?)", (tuple of values))
# c.execute("INSERT INTO stats VALUES (:teams, ..., :rushing_yards)", ('teams': value, ..., 'rushing_yards': value))

c.execute("SELECT * FROM stats WHERE teams='TestTeam'")

# c.fetchone(), c.fetchmany(numer of rows to fetch), c.fetchall()
# use after each select statement to use selected data (I think)
print(c.fetchone())

#finishes transaction
connection.commit()

connection.close()

# This may be useful later
#df = pandas.read_csv(csvfile)
#df.to_sql(table_name, conn, if_exists='append', index=False)
