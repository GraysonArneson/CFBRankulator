import csv
import sqlite3

connection = sqlite3.connect('rankulator.db')
c = connection.cursor()
teamData = c.execute("SELECT * FROM team")
with open('Rankings.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    #writer.writerow(['name', 'AVGsuccPCT', 'AVG_PPP', 'Score', 'AVGdefSuccPct', 'AVG_DefPPP', 'DefScore', 'SOS', 'Adjusted_Score'])
    writer.writerow(['name', 'AVGsuccPCT', 'AVG_PPP', 'Score', 'SOS', 'Adjusted_Score'])
    writer.writerows(teamData)

connection.close()
