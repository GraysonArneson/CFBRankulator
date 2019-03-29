import json, requests
import pandas as pd
#Home scores at the 100, starts AT WORST at the 1. Inverse for away teams, dealt with below
d = {
  1 : 0.742, 2 : 0.797, 3 : 0.806, 4 : 0.827, 5 : 0.842, 6 : 0.853, 7 : 0.866, 8 : 0.877, 9 : 0.899, 10 : 0.908, 11 : 0.910, 12 : 0.914, 13 : 0.932, 14 : 0.942,
  15 : 0.951, 16 : 0.991, 17 : 1.062, 18 : 1.141, 19 : 1.176, 20 : 1.179, 21 : 1.186, 22 : 1.188, 23 : 1.192, 24 : 1.233, 25 : 1.243,
  26 : 1.270, 27 : 1.306, 28 : 1.350, 29 : 1.407, 30 : 1.446, 31 : 1.489, 32 : 1.514, 33 : 1.550, 34 : 1.566, 35 : 1.579, 36 : 1.608,
  37 : 1.629, 38 : 1.643, 39 : 1.711, 40 : 1.746, 41 : 1.756, 42 : 1.794, 43 : 1.835, 44 : 1.839, 45 : 1.916, 46 : 1.942, 47 : 1.979,
  48 : 2.008, 49 : 2.067, 50 : 2.095, 51 : 2.168, 52 : 2.219, 53 : 2.271, 54 : 2.286, 55 : 2.341, 56 : 2.377, 57 : 2.413, 58 : 2.477,
  59 : 2.580, 60 : 2.620, 61 : 2.712, 62 : 2.815, 63 : 2.880, 64 : 2.924, 65 : 3.061, 66 : 3.088, 67 : 3.150, 68 : 3.226, 69 : 3.301,
  70 : 3.334, 71 : 3.409, 72 : 3.491, 73 : 3.572, 74 : 3.645, 75 : 3.706, 76 : 3.782, 77 : 3.826, 78 : 3.842, 79 : 3.887, 80 : 3.898,
  81 : 3.976, 82 : 4.031, 83 : 4.065, 84 : 4.134, 85 : 4.253, 86 : 4.280, 87 : 4.313, 88 : 4.340, 89 : 4.382, 90 : 4.411, 91 : 4.457,
  92 : 4.576, 93 : 4.752, 94 : 4.854, 95 : 4.993, 96 : 5.201, 97 : 5.394, 98 : 5.484, 99 : 5.625, 100 : 6.963
}
#Call API for week 6 Florida game
weeks = ["6"]
# weeks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
# teams = ["Florida", "Miami", "Georgia", "NC State", "Arkansas", "Mississippi State", "Texas A&M", "South Carolina", "Ole Miss"]
# teams = ["Florida", "LSU", "Florida State", "Alabama"]
# teams = ["Florida", "LSU"]
#SEC = ["Florida"]

home = []
SEC = ["Florida", "LSU", "Texas A&M", "Alabama", "Arkansas", "Auburn", "Georgia", "Kentucky", "Mississippi State", "Missouri", "Ole Miss", "South Carolina", "Tennessee", "Vanderbilt"]
ACC = ["Florida State", "Boston College", "Clemson", "Duke", "Georgia Tech", "Louisville", "Miami", "NC State", "Pittsburgh", "Syracuse", "North Carolina", "Virginia", "Virginia Tech", "Wake Forest", "Notre Dame"]
PAC = ["Arizona", "Arizona State", "California", "Colorado", "Oregon", "Oregon State", "Stanford", "UCLA", "USC", "Utah", "Washington", "Washington State"]
B1G = ["Illinois", "Indiana", "Iowa", "Maryland", "Michigan", "Michigan State", "Minnesota", "Nebraska", "Northwestern", "Ohio State", "Penn State", "Purdue", "Rutgers", "Wisconsin"]
B12 = ["Baylor", "Iowa State", "Kansas", "Kansas State", "Oklahoma", "Oklahoma State", "TCU", "Texas", "Texas Tech", "West Virginia"]
teams = SEC
allP5 = []
allP5.extend(SEC)
allP5.extend(ACC)
allP5.extend(PAC)
allP5.extend(B1G)
allP5.extend(B12)
# teams.extend(ACC)
# teams.extend(PAC)
# teams.extend(B1G)
# teams.extend(B12)

#Make API call

weekNum = []
teamName = []
numRush = []
succRush = []
numPass = []
succPass = []
succPct = []
numPlays = []
PointsPerPlay = []

week = 13
toGet = "https://api.collegefootballdata.com/plays?seasonType=regular&year=2018&week=" + str(week)

# response = requests.get("https://api.collegefootballdata.com/plays?seasonType=regular&year=2018&week=5")
response = requests.get(toGet)

#Check for appropriate response code
print("Received status code: " + str(response.status_code))
print("Expected status code: 200")

#Create dataframe
df = pd.read_json(response.content)
df.sort_values(by=['period'])
df.to_csv('raw_results.csv')


toSkip = ["Kickoff", "Punt", "Penalty", "Timeout", "End Period", "Fumble Recovery (Opponent)", "Field Goal Missed", "Field Goal Good", "End of Half", "Blocked Punt", "Blocked Field Goal", "Kickoff Return Touchdown", "Missed Field Goal Return", "Safety", "Uncategorized"]

# for index, row in df.iterrows():
#     if(row['play_type'] == "Kickoff"):
#         if(row['yard_line'] == 35):
#             #home.insert('1', teams.index(team))
#             home.append('1')
#         elif(row['yard_line'] == 65):
#             #home.insert('0', teams.index(team))
#             home.append('0')
#         else
#             continue
#Sort through teams in specific week
for team in teams:
    PassSuccess = 0
    PassTotal = 0
    RushSuccess = 0
    RushTotal = 0
    PPP = 0
    homeT = False
    checkSkip = False
    #Figure out away vs home team
    for index, row in df.iterrows():
        #Check if non-P5 opponent
        if row['defense'] not in allP5 and (row['offense'] == team):
            print(team + " played a non-P5 opponent this week")
            checkSkip = True
            break
        if(row['play_type'] == "Kickoff") and (row['offense'] == team):
            if(row['yard_line'] == 35):
                #home.insert('1', teams.index(team))
                homeT = True
                break
            elif(row['yard_line'] == 65) and (row['offense'] == team):
                #home.insert('0', teams.index(team))
                break
            else:
                continue
    for index, row in df.iterrows():
        #Skip calculations if going to skip later
        if checkSkip == True:
            break
        #Get yardline for home vs away
        if homeT == True:
            var_yardline = row['yard_line']
        else:
            var_yardline = 100-row['yard_line']
        #Eliminate garbage time scores
        if row['period'] == 2 and abs(row['defense_score'] - row['offense_score']) >= 38:
            continue
        if row['period'] == 3 and abs(row['defense_score'] - row['offense_score']) >= 28:
            continue
        if row['period'] == 4 and abs(row['defense_score'] - row['offense_score']) >= 22:
            continue
        #Skip when team is not on offense
        if row['offense'] != team:
            continue
        #Skip if any of the following plays
        elif row['play_type'] in toSkip:
            continue

        #Calculate Points Per Play
        tempPPP = 0
        if var_yardline + row['yards_gained'] > 100:
            tempPPP = d[100] - d[var_yardline]
        elif var_yardline + row['yards_gained'] < 0:
            tempPPP = d[1] - d[var_yardline]
        elif (var_yardline + row['yards_gained'] == 0) or var_yardline == 0 or var_yardline == 100:
            tempPPP = 0
        else:
            tempPPP = d[var_yardline + row['yards_gained']] - d[var_yardline]
        PPP += tempPPP
        #Rushing logic for success rate
        if row['play_type'] == "Rush":
            RushTotal += 1
            if (row['distance'] - row['yards_gained'] <= 5 and row['down'] == 1) or (row['distance'] - row['yards_gained'] <= 3 and row['down'] == 2) or (row['distance'] - row['yards_gained'] <= 0 and (row['down'] == 3 or row['down'] == 4)):
                RushSuccess += 1
        #Punish rushing game for sacks and fumbles
        elif row['play_type'] == "Fumble Recovery (Own)" or row['play_type'] == "Sack":
            RushTotal += 1
        #Passing logic for success rate
        elif row['play_type'] == "Pass Reception":
            PassTotal += 1
            if (row['distance'] - row['yards_gained'] <= 5 and row['down'] == 1) or (row['distance'] - row['yards_gained'] <= 3 and row['down'] == 2) or (row['distance'] - row['yards_gained'] <= 0 and (row['down'] == 3 or row['down'] == 4)):
                PassSuccess += 1
        #Punish incompletions and interceptions
        elif row['play_type'] == "Pass Interception Return" or row['play_type'] == "Interception Return Touchdown" or row['play_type'] == "Pass Incompletion":
            PassTotal += 1
        #Reward touchdowns
        elif row['play_type'] == "Rushing Touchdown":
            RushTotal += 1
            RushSuccess += 1
        elif row['play_type'] == "Passing Touchdown":
            PassTotal += 1
            PassSuccess += 1
        else:
            continue;
    # rushing success rate (rsr)
    # passing success rate (psr)
    # succ rate(sr)
    # final points per play (fppp)
    if RushTotal == 0 and PassTotal == 0:
        print(team + " didn't play this week")
        continue
    elif checkSkip == True:
        continue
    teamName.append(team)
    weekNum.append(week)
    rsr = str((RushSuccess/RushTotal)*100)
    psr = str((PassSuccess/PassTotal)*100)
    sr = str(((RushSuccess+PassSuccess)/(RushTotal+PassTotal))*100)
    fppp = str(PPP/(RushTotal+PassTotal)*100)

    score = float(fppp) + float(sr)

    print("FINAL " + team + " RUSH SUCCESS RATE: " + rsr + "%")
    print("Pass Total: " + str(PassTotal) + "\nPass Success: " + str(PassSuccess))
    print("FINAL "  + team + " PASS SUCCESS RATE: " + psr + "%")
    print("TOTAL " + team + " SUCCESS RATE: " + sr + "%")
    print("FINAL " + team + " PPP: " + str(PPP/(RushTotal+PassTotal)))
    print("TEAM SCORE FOR OFFENSE: " + str(score))
    print("")
    print("---------------------------------------------------------------------------------------")
    Pct1 = (((RushSuccess+PassSuccess)/(RushTotal+PassTotal))*100)
    totalPlays = RushTotal + PassTotal
    toAppend = PPP/totalPlays
    numRush.append(RushTotal)
    succRush.append(RushSuccess)
    numPass.append(PassTotal)
    succPass.append(PassSuccess)
    succPct.append(Pct1)
    numPlays.append(totalPlays)
    PointsPerPlay.append(toAppend)
    if homeT == True:
        home.append('1')
    else:
        home.append('0')

#Convert dataframe to csv
print(teamName)
print(weekNum)
print(numRush)
print(succRush)
list_of_tuples = list(zip(weekNum, teamName, numRush, succRush, numPass, succPass, succPct, numPlays, PointsPerPlay))
df2 = pd.DataFrame(list_of_tuples, columns = ['weekNum', 'teamName', 'numRush', 'succRush', 'numPass', 'succPass', 'succPct', 'numPlays', 'PointsPerPlay'])
df2.to_csv('testCombine.csv', index=False)
#df2.to_csv("test.csv", if_exists='append', index=False)
df.to_csv('raw_results.csv')
