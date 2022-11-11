import regional as r
import pickle

f = open("Regional Data 22-04-2022 H11 M09 S14.pickle", 'rb')

regional: r.regional=pickle.load(f)

f.close()

t: r.team = regional.teamList['3970']
print(t.matchList)

print(t.levels)
