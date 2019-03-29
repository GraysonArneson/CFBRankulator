import sqlite3
import pandas as pd
import RankulatorLib as RL

connection = sqlite3.connect('rankulator.db')
#connection = sqlite3.connect(':memory:')

c = connection.cursor()
#insert the values for the new week
RL.insert_table_data('testCombine.csv', connection, 'stats')

#Update all values in team table except SOS
RL.update_team_table(connection, c)
connection.close()
