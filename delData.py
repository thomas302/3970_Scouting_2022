import pickle
import regional as r

f = open(r'C:\Users\mract\Desktop\Programming\PythonProjects\2022_Scouting\Regional Data 21-04-2022 H12 M23 S46.pickle', 'rb')

regional: r.regional = pickle.load(f)

f.close()

team: r.team = regional.teamList['316']

match: r.match

count = 0
for match in team.matchList:
    if match.data.matchNumber == 37:
        team.matchList.pop(count)
    count += 1;

for match in team.matchList:
    print(match.data.matchNumber)


