import json, requests
import pandas as pd
#Home scores at the 100, starts AT WORST at the 1
d = {
  1 : 0.742, 2 : 0.797, 3 : 0.806, 4 : 0.827, 5 : 0.842, 6 : 0.853, 7 : 0.866, 8 : 0.877, 9 : 0.899, 10 : 0.908, 11 : 0.910, 12 : 0.914, 13 : 0.932, 14 : 0.942,
  15 : 0.951, 16 : 0.991, 17 : 1.062, 18 : 1.141, 19 : 1.176, 20 : 1.179, 21 : 1.186, 22 : 1.188, 23 : 1.192, 24 : 1.233, 25 : 1.243,
  26 : 1.270, 27 : 1.306, 28 : 1.350, 29 : 1.407, 30 : 1.446, 31 : 1.489, 32 : 1.514, 33 : 1.550, 34 : 1.566, 35 : 1.579, 36 : 1.608,
  37 : 1.629, 38 : 1.643, 39 : 1.711, 40 : 1.746, 41 : 1.756, 42 : 1.794, 43 : 1.835, 44 : 1.839, 45 : 1.916, 46 : 1.942, 47 : 1.979,
  48 : 2.008, 49 : 2.067, 50 : 2.095, 51 : 2.168, 52 : 2.219, 53 : 2.271, 54 : 2.286, 55 : 2.341, 56 : 2.377, 57 : 2.413, 58 : 2.477,
  59 : 2.580, 60 : 2.620, 61 : 2.712, 62 : 2.815, 63 : 2.880, 64 : 2.924, 65 : 3.061, 66 : 3.088, 67 : 3.150, 68 : 3.226, 69 : 3.301,
  70 : 3.334, 71 : 3.409, 72 : 3.491, 73 : 3.572, 74 : 3.645, 75 : 3.706, 76 : 3.782, 77 : 3.826, 78 : 3.842, 79 : 3.887, 80 : 3.898,
  81 : 3.976, 82 : 4.031, 83 : 4.065, 84 : 4.134, 85 : 4.253, 86 : 4.280, 87 : 4.313, 88 : 4.340, 89 : 4.382, 90 : 4.411, 91 : 4.457,
  92 : 4.576, 93 : 4.752, 94 : 4.854, 95 : 4.993, 96 : 5.201, 97 : 5.394, 98 : 5.484, 99 : 5.625, 100 : 6.963, 136:7
}
#Call API for week 6 Florida game
weeks = ["6"]
# weeks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
teams = ["Florida"]
# teams = ["Florida", "LSU", "Florida State", "Alabama"]
# SEC = ["Florida", "LSU", "Texas A&M", "Alabama", "Arkansas", "Auburn", "Georgia", "Kentucky", "Mississippi State", "Missouri", "Ole Miss", "South Carolina", "Tennessee", "Vanderbilt"]
# ACC = ["Florida State", "Boston College", "Clemson", "Duke", "Georgia Tech", "Louisville", "Miami", "NC State", "Pittsburgh", "Syracuse", "Virginia", "Virginia Tech", "Wake Forest"]
# PAC = ["Arizona", "Arizona State", "California", "Colorado", "Oregon", "Oregon State", "Stanford", "UCLA", "USC", "Utah", "Washington", "Washington State"]
# B1G = ["Illinois", "Indiana", "Iowa", "Maryland", "Michigan", "Michigan State", "Minnesota", "Nebraska", "Northwestern", "Ohio State", "Penn State", "Purdue", "Rutgers", "Wisconsin"]
# B12 = ["Baylor", "Iowa State", "Kansas", "Kansas State", "Oklahoma", "Oklahoma State", "TCU", "Texas", "Texas Tech", "West Virginia"]
# teams = SEC
# teams.extend(ACC)
# teams.extend(PAC)
# teams.extend(B1G)
# teams.extend(B12)

#Make API call
response = requests.get("https://api.collegefootballdata.com/plays?seasonType=regular&year=2018&week=6")

#Check for appropriate response code
print("Received status code: " + str(response.status_code))
print("Expected status code: 200")

#Create dataframe
df = pd.read_json(response.content)
df.sort_values(by=['period'])

#Sort through teams in specific week
for team in teams:
    PassSuccess = 0
    PassTotal = 0
    RushSuccess = 0
    RushTotal = 0
    PPP = 0
    for index, row in df.iterrows():
        #Skip when team is not on offense
        if row['offense'] != team:
            continue;
        #Skip if any of the following plays
        elif row['play_type'] == "Kickoff" or row['play_type'] == "Punt" or row['play_type'] == "Penalty" or row['play_type'] == "Timeout" or row['play_type'] == "End Period":
            continue;
        #Rushing logic for success rate
        elif row['play_type'] == "Rush" and row['offense'] == team:
            if row['distance'] - row['yards_gained'] <= 5 and row['down'] == 1:
                RushSuccess += 1
                RushTotal += 1
                PPP += d[row['yard_line']+row['yards_gained']] - d[row['yard_line']]
            elif row['distance'] - row['yards_gained'] <= 3 and row['down'] == 2:
                RushSuccess += 1
                RushTotal += 1
                PPP += d[row['yard_line']+row['yards_gained']] - d[row['yard_line']]
            elif row['distance'] - row['yards_gained'] <= 0 and (row['down'] == 3 or row['down'] == 4):
                RushSuccess += 1
                RushTotal += 1
                PPP += d[row['yard_line']+row['yards_gained']] - d[row['yard_line']]
            else:
                RushTotal += 1
        #Punish rushing game for sacks
        elif row['play_type'] == "Sack":
            RushTotal += 1
        #Reward touchdowns
        elif row['play_type'] == "Rushing Touchdown":
            RushSuccess += 1
            RushTotal += 1
            PPP += d[row['yard_line']+row['yards_gained']] - d[row['yard_line']]
        elif row['play_type'] == "Pass Reception" or row['play_type'] == "Passing Touchdown":
            PassSuccess += 1
            PassTotal += 1
            PPP += d[row['yard_line']+row['yards_gained']] - d[row['yard_line']]
        #Punish incompletions
        elif row['play_type'] == "Pass Incompletion":
            PassTotal += 1
        else:
            continue;

    print("FINAL " + team + " RUSH SUCCESS RATE: " + str((RushSuccess/RushTotal)*100) + "%")
    print("FINAL "  + team + " PASS SUCCESS RATE: " + str((PassSuccess/PassTotal)*100) + "%")
    print("TOTAL " + team + " SUCCESS RATE: " + str(((RushSuccess+PassSuccess)/(RushTotal+PassTotal))*100) + "%")
    print("FINAL " + team + " PPP: " + str(PPP/(RushTotal+PassTotal)))
    print("---------------------------------------------------------------------------------------")

#Convert dataframe to csv
#df.to_csv('results.csv')