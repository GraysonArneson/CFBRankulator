import sqlite3
import pandas as pd
import RankulatorLib as RL

#SOS = {"LSU" : 1.2, "Tennessee" : 1.19384615385, "Auburn" : 1.1876923077, "Texas A&M" : 1.18153846155, "Arkansas" : 1.1753846154, "Ole Miss" : 1.16923076925, "South Carolina" : 1.1630769231, "Mississippi State" : 1.15692307695, "Georgia" : 1.1507692308, "Missouri" : 1.14461538465, "Alabama" : 1.1384615385, "Kentucky" : 1.13230769235, "Vanderbilt" : 1.1261538462, "Florida" : 1.12000000005, "UCLA" : 1.1138461539, "Louisville" : 1.10769230775, "Pittsburgh" : 1.1015384616, "Florida State" : 1.09538461545, "Northwestern" : 1.0892307693, "Maryland" : 1.08307692315, "Indiana" : 1.076923077, "Kansas State" : 1.07076923085, "Georgia Tech" : 1.0646153847, "Texas" : 1.05846153855, "TCU" : 1.0523076924, "Michigan" : 1.04615384625, "Purdue" : 1.0400000001, "Michigan State" : 1.03384615395, "Penn State" : 1.0276923078, "Nebraska" : 1.02153846165, "Rutgers" : 1.0153846155, "Oregon State" : 1.00923076935, "Stanford" : 1.0030769232, "Washington" : 0.99692307705, "Minnesota" : 0.9907692309, "Texas Tech" : 0.98461538475, "Iowa State" : 0.9784615386, "Utah" : 0.97230769245, "West Virginia" : 0.9661538463, "Baylor" : 0.96000000015, "Wake Forest" : 0.953846154, "Kansas" : 0.94769230785, "USC" : 0.9415384617, "Arizona State" : 0.93538461555, "Oklahoma State" : 0.9292307694, "Boston College" : 0.92307692325, "Syracuse" : 0.9169230771, "Wisconsin" : 0.91076923095, "Ohio State" : 0.9046153848, "Duke" : 0.89846153865, "Washington State" : 0.8923076925, "Colorado" : 0.88615384635, "Notre Dame" : 0.8800000002, "California" : 0.87384615405, "Oregon" : 0.8676923079, "Illinois" : 0.86153846175, "Oklahoma" : 0.8553846156, "Iowa" : 0.84923076945, "Clemson" : 0.8430769233, "NC State" : 0.83692307715, "Arizona" : 0.830769231, "Virginia Tech" : 0.82461538485, "Miami" : 0.8184615387, "North Carolina" : 0.81230769255, "Virginia" : 0.8061538464}

#In memory db ':memory:; lives in RAM; useful for testing b/c fresh start each time
connection = sqlite3.connect('rankulator.db')
#connection = sqlite3.connect(':memory:')

c = connection.cursor()

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
             PointsPerPlay real,
             defSucc real,
             defPointsPerPlay real
             )""")

RL.insert_table_data('testCombine.csv', connection, 'stats')

# Team(name, AVGsuccPCT, AVG_PPP, Score, SOS, Adjusted_Score)
c.execute("""CREATE TABLE team (
             name text,
             AVGsuccPct real,
             AVG_PPP real,
             Score real,
             AVGdefSuccPct real,
             AVG_DefPPP real,
             DefScore real,
             SOS real DEFAULT 1,
             Adjusted_Score real DEFAULT NULL
             )""")

#Initialize team table with all teams and 0 values for each metric
RL.insert_table_data('teamInit.csv', connection, 'team')

#Update the Strength of Schedule for each team
RL.update_SOS(connection, c)

#Update metrics and ranking scores for each team
RL.update_team_table(connection, c)

connection.close()
