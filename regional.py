from statistics import multimode
import uuid 

class matchData: 
    def __init__(self, mainList = list()):
        self.mainList = mainList
        self.matchNumber = 0 if not self.mainList[0].isnumeric() else int(self.mainList[0])
        self.teamNumber = self.mainList[1]
        print(self.teamNumber)
        self.taxi = (True if self.mainList[2] == 'true' else False if self.mainList[2] == 'false' else None)
        self.autoShotsTaken = 0 if '' == self.mainList[3] else int(self.mainList[3])
        self.autoShotsHigh = 0 if '' == self.mainList[4] else int(self.mainList[4])
        self.autoShotsLow = 0 if '' == self.mainList[5] else int(self.mainList[5])
        self.twoBall = (True if self.mainList[6] == 'true' else False if self.mainList[6] == 'false' else None)
        self.teleShotsTaken = 0 if '' == self.mainList[7] else int(self.mainList[7])
        self.teleShotsHigh = 0 if '' == self.mainList[8] else int(self.mainList[8])
        self.teleShotsLow = 0 if '' == self.mainList[9] else int(self.mainList[9])
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
        self.uuid = uuid.uuid4()
        
class team():
    def __init__(self, teamNumber):
        self.teamNumber = teamNumber
        self.matchList = []

    def addMatch(self, m: match):
        self.matchList.append(m)
    
    def updateAutoData(self, filterFunc=lambda x: True):
        matchList = list(filter(filterFunc, self.matchList))
        autoShotsTaken = 0
        autoShotsLow = 0
        autoShotsHigh = 0
        autoShotsMade = 0
        taxi = False
        taxi_count = 0

        m:match
        for m in matchList:
            autoShotsTaken += m.data.autoShotsTaken
            autoShotsHigh += m.data.autoShotsHigh
            autoShotsLow += m.data.autoShotsLow
            autoShotsMade += m.data.autoShotsLow + m.data.autoShotsHigh
            if m.data.taxi:
                taxi_count += 1
                taxi = True

        self.taxi = taxi if taxi_count > 0 else False
        
        if not autoShotsMade == 0:
            addHigh = (autoShotsTaken-autoShotsMade) * (autoShotsHigh/autoShotsMade) if not autoShotsTaken == 0 else 0
            addLow = (autoShotsTaken-autoShotsMade) * (autoShotsLow/autoShotsMade) if not autoShotsTaken == 0 else 0
            self.autoAverageHigh = ((autoShotsHigh+addHigh)/len(matchList))
            self.autoAverageLow = ((autoShotsLow+addLow)/len(matchList))
            self.autoShotPercentage = (autoShotsLow + autoShotsHigh)/autoShotsMade
        else:
            self.autoAverageLow = 0
            self.autoAverageHigh = 0
            self.autoShotPercentage = 0

        self.taxi_score = 0 if len(matchList) == 0 else (taxi_count/len(matchList))*2

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
        
        if not (shotsTaken == 0):
            self.shotPercentage = (shotsMade/shotsTaken)
            
            addHigh = (shotsTaken-shotsMade) * (shotsHigh/shotsTaken)
            addLow = (shotsTaken-shotsMade) * (shotsLow/shotsTaken)

            self.averageShotsHigh = ((shotsHigh+addHigh)/len(matchList))
            self.averageShotsLow = ((shotsLow+addLow)/len(matchList))
        else:
            self.shotPercentage = 0
            self.averageShotsHigh = 0
            self.averageShotsLow = 0

    def updateClimbData(self, filterFunc=lambda x:True):
        matchList = list(filter(filterFunc, self.matchList))
        noClimb = ["No Climb", 0, 0]
        attempt = ["Attempt", 0, 0]
        level_1 = ["Level 1", 0, 0]
        level_2 = ["Level 2", 0, 0]
        level_3 = ["Level 3", 0, 0]
        level_4 = ["Level 4", 0, 0]
        
        m: match
        for m in matchList:
            if m.data.climbLevel == -1:
                noClimb[1] += 1
            if m.data.climbLevel == 0:
                attempt[1] += 1
            if m.data.climbLevel == 1:
                level_1[1] += 1
            if m.data.climbLevel == 2:
                level_2[1] += 1
            if m.data.climbLevel == 3:
                level_3[1] += 1
            if m.data.climbLevel == 4:
                level_4[1] += 1

        levels = [
                  noClimb,
                  attempt,
                  level_1,
                  level_2,
                  level_3,
                  level_4,
                 ]

        levels = sorted(levels, key=lambda x: x[1], reverse=True)
        
        self.high_plus_percent = 0

        for level in levels:
            level[2] = level[1]/len(matchList)

            if level[0] == 'Level 3' or level[0] == 'Level 4':
                self.high_plus_percent += level[2]

        self.levels = levels


    def calcAverageTelePoints(self):
        self.averageTelePoints = (self.averageShotsLow + 2 * self.averageShotsHigh) * self.shotPercentage

    def calcAverageAutoPoints(self):
        self.averageAutoPoints = (2 * self.autoAverageLow + 4 * self.autoAverageHigh) * self.autoShotPercentage + self.taxi_score

    def appendMatchList(self, matchList: list()):
        m: match
        for m in matchList:
            self.matchList.append(m)

    def rmMatch(self, matchNo, teamNo):
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
            f = lambda x: (x.data.matchNumber) >= matchThreshold
        
        teams = [] 

        for k, t in self.teamList.items():
            t.updateShotData(f)
            t.calcAverageTelePoints()

            if t.averageTelePoints >= shotThreshold:
                teams.append(t)
         
        t: team
        self.teamsOverShotThreshold = list(sorted(teams, key=lambda t: t.averageTelePoints, reverse=True))

    def updateAutoData(self, matchThreshold=None):
        if matchThreshold == None:
            f = lambda x: True
        else:
            x: match
            f = lambda x: (x.data.matchNumber) >= matchThreshold
        
        t: team
        for k, t in self.teamList.items():
            t.updateAutoData(f)
            t.calcAverageAutoPoints()

    def updateClimbData(self, matchThreshold=None):
        if matchThreshold == None:
            f = lambda x: True
        else:
            x: match
            f = lambda x: (x.data.matchNumber) >= matchThreshold

        t: team
        for k, t in self.teamList.items():
            t.updateClimbData()
        
 
    # TODO
    def getTeamsOverClimbThreshold(self, level, percent = None):
        pass
