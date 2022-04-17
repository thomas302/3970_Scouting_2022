from dataclasses import dataclass
from statistics import multimode
import pickle

@dataclass
class matchData:
    mainList: list
    def __init__(self):
        matchNumber = self.mainList[0]
        teamNumber = self.mainList[1]
        taxi = (True if self.mainList[2] == 'true' else False if self.mainList[2] == 'false' else None)
        autoShotsTaken = int(self.mainList[3])
        autoShotsHigh = int(self.mainList[4])
        autoShotsLow = int(self.mainList[5])
        twoBall = (True if self.mainList[6] == 'true' else False if self.mainList[6] == 'false' else None)
        teleShotsTaken = int(self.mainList[7])
        teleShotsHigh = int(self.mainList[8])
        teleShotsLow = int(self.mainList[9])
        stoppedFromScoring = (True if self.mainList[10] == 'true' else False if self.mainList[10] == 'false' else None)
        defense = (True if self.mainList[11] == 'true' else False if self.mainList[11] == 'false' else None) 
        endgameShooting = (True if self.mainList[12] == 'true' else False if self.mainList[12] == 'false' else None)
        climbLevel = int(self.mainList[13])
        disabled = self.mainList[14]
        mainFocus = self.mainList[15].split(',')

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

    def addMatch(self, match: match):
        self.matchList.append(match)
    
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
        matchList = filter(filterFunc, self.matchList)
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

        self.shotPercentage = (shotsMade/shotsTaken)
        
        addHigh = (shotsTaken-shotsMade) * (shotsHigh/shotsTaken)
        addLow = (shotsTaken-shotsMade) * (shotsLow/shotsTaken)

        self.averageShotsHigh = ((shotsHigh+addHigh)/len(matchList))
        self.averageShotsLow = ((shotsLow+addLow)/len(matchList))

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
        self.rawMatchList = [["Raw Data", "Defense Comments", "Catastrophe Comments", "Other Comments"]]

    def addTeam(self, teamNumber):
        if not teamNumber in self.teamList:
            self.teamList[teamNumber] = team(teamNumber)
        else:
            raise Team_In_List("That team is already in the Teams List")

    def addNewMatch(self, match: match):
        if not match.data.teamNumber in self.teamList:
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
        
        for t in self.teamList:
            self.teamList[t].updateShotData(f)
            self.teamList[t].calcAverageTelePoints()

            if t.averageTelePoints >= shotThreshold:
                teams.append(t)
        
        t: team
        return teams.sort(key=lambda t: t.averageTelePoints, reverse=True)
    
    # TODO
    def getTeamsOverClimbThreshold(self, level, percent = None):
        pass 
