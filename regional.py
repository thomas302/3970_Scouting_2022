from dataclasses import dataclass
from statistics import multimode

class matchData: 
    def __init__(self, mainList = list()):
        self.mainList = mainList
        self.matchNumber = self.mainList[0]
        self.teamNumber = self.mainList[1]
        print(self.teamNumber)
        self.taxi = (True if self.mainList[2] == 'true' else False if self.mainList[2] == 'false' else None)
        self.autoShotsTaken = int(self.mainList[3])
        self.autoShotsHigh = int(self.mainList[4])
        self.autoShotsLow = int(self.mainList[5])
        self.twoBall = (True if self.mainList[6] == 'true' else False if self.mainList[6] == 'false' else None)
        self.teleShotsTaken = int(self.mainList[7])
        self.teleShotsHigh = int(self.mainList[8])
        self.teleShotsLow = int(self.mainList[9])
        self.stoppedFromScoring = (True if self.mainList[10] == 'true' else False if self.mainList[10] == 'false' else None)
        self.defense = (True if self.mainList[11] == 'true' else False if self.mainList[11] == 'false' else None) 
        self.endgameShooting = (True if self.mainList[12] == 'true' else False if self.mainList[12] == 'false' else None)
        self.climbLevel = int(self.mainList[13])
        self.disabled = self.mainList[14]
        self.mainFocus = self.mainList[15].split(',')

class match():
    def __init__(self, data: matchData, defenseComments, catastropheComments, otherComments):
        self.data = data
        self.defenseComments = defenseComments
        self.catastropheComments = catastropheComments
        self.otherComments = otherComments
        
class team():
    def __init__(self, teamNumber):
        self.teamNumber = teamNumber
        self.matchList = []

    def addMatch(self, m: match):
        self.matchList.append(m)
    
    def updateAutoData(self, filterFunc=lambda x: True):
        matchList = filter(filterFunc, self.matchList)
        autoShotsTaken = 0
        autoShotsLow = 0
        autoShotsHigh = 0
        autoShotsMade = 0
        taxi = False

        m:match
        for m in matchList:
            autoShotsTaken += m.data.autoShotsTaken
            autoShotsHigh += m.data.autoShotsHigh
            autoShotsLow += m.data.autoShotsLow
            autoShotsMade += m.data.autoShotsLow + m.data.autoShotsHigh
            if m.data.taxi:
                taxi = True

        self.taxi = taxi

        self.autoShotPercentage = (autoShotsMade/autoShotsTaken)
        addHigh = (autoShotsTaken-autoShotsMade) * (autoShotsHigh/autoShotsMade)
        addLow = (autoShotsTaken-autoShotsMade) * (autoShotsLow/autoShotsMade)
        self.autoAverageHigh = ((autoShotsHigh+addHigh)/len(matchList))
        self.autoAverageLow = ((autoShotsLow+addLow)/len(matchList))



    def updateShotData(self, filterFunc=lambda x: True):
        matchList = list(filter(filterFunc, self.matchList))
        shotsTaken = 0
        shotsMade = 0
        shotsHigh = 0
        shotsLow = 0

        m:match
        for m in matchList:
            shotsTaken += m.data.teleShotsTaken
            shotsMade += (m.data.teleShotsHigh+m.data.teleShotsLow)
            shotsHigh += (m.data.teleShotsHigh)
            shotsLow += (m.data.teleShotsLow)
        
        if not shotsTaken == 0:
            self.shotPercentage = (shotsMade/shotsTaken)
            
            addHigh = (shotsTaken-shotsMade) * (shotsHigh/shotsTaken)
            addLow = (shotsTaken-shotsMade) * (shotsLow/shotsTaken)

            self.averageShotsHigh = ((shotsHigh+addHigh)/len(matchList))
            self.averageShotsLow = ((shotsLow+addLow)/len(matchList))
        else:
            self.shotPercentage = 0
            self.averageShotsHigh = 0
            self.averageShotsLow = 0


    def calcAverageTelePoints(self):
        self.averageTelePoints = (self.averageShotsLow + 2 * self.averageShotsHigh)*self.shotPercentage

    def calcAverageAutoPoints(self):
        pass

class Team_In_List(ValueError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class regional():
    def __init__(self):
        self.teamList: dict(int, team) = dict()
        self.rawMatchList = list()

    def addTeam(self, teamNumber):
        if not teamNumber in self.teamList.keys():
            self.teamList[teamNumber] = team(teamNumber)
        else:
            raise Team_In_List("That team is already in the Teams List")

    def addNewMatch(self, match: match):
        if not match.data.teamNumber in self.teamList.keys():
            self.addTeam(match.data.teamNumber)

        t: team = self.teamList[match.data.teamNumber]
        t.addMatch(match)


    def getTeamsOverTelePointThreshold(self, shotThreshold, matchThreshold = None):
        if matchThreshold == None:
            f = lambda x: True
        else:
            x: match
            f = lambda x: x.data.matchNumber >= matchThreshold
        
        teams = []
        

        for k, t in self.teamList.items():
            t.updateShotData(f)
            t.calcAverageTelePoints()

            if t.averageTelePoints >= shotThreshold:
                teams.append(t)
         
        t: team
        self.teamsOverShotThreshold = list(sorted(teams, key=lambda t: t.averageTelePoints, reverse=True))
    
    # TODO
    def getTeamsOverClimbThreshold(self, level, percent = None):
        pass 
