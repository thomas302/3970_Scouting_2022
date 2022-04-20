import pickle

import regional as r

f = open("Regional Data 19-04-2022 H22 M48 S51.pickle", 'rb')

regional: r.regional = pickle.load(f)

f.close()

print(regional.rawMatchList)
