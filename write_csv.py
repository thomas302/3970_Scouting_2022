import pickle
import csv

import regional as r

f = open('.\\Regional Data 12-11-2022 H18 M25 S15.pickle','rb')

regional: r.regional = pickle.load(f)

f.close()

csvFile = open(".\\matchData.csv", 'w')

csvFile.write('; '.join(["Match number", 'Team Number', 'Taxi', 'Auto Shots High', 'Auto Shots Low', 'Auto Shots Taken', "Two Ball", "Tele Shots High", "Tele Shots Low", 'Tele Shots Taken', 'Defense', 'Disabled', 'Main Focus', 'Endgame Shooting', 'Climb Level', 'Defense Comments', 'Catastrophe Comments', 'Other Comments \n']))

for l in regional.rawMatchList:
    m: r.match = l[0]
    d: r.matchData = m.data
    row = [
            str(d.matchNumber),
            str(d.teamNumber),
            str(d.taxi),
            str(d.autoShotsHigh),
            str(d.autoShotsLow),
            str(d.autoShotsTaken), 
            str(d.twoBall),
            str(d.teleShotsHigh),
            str(d.teleShotsLow),
            str(d.teleShotsTaken), 
            str(d.defense),
            str(d.disabled),
            str(d.mainFocus),
            str(d.endgameShooting),
            str(d.climbLevel),
            str(l[1]),
            str(l[2]),
            str(l[3])+'\n'
            ]
    csvFile.write('; '.join(row))


print(regional.rawMatchList)
csvFile.close()
