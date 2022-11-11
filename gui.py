import PySimpleGUI as sg
import fileinput as fi
import csv
import pickle
import os
import datetime as d
import traceback
import regional as r
import time

from datetime import datetime
from io import StringIO

PST_timezone = d.timezone(d.timedelta(hours=-8))
regional = r.regional()

def pickleRegional():
    dt = datetime.now()
    dt_string = ''.join(dt.strftime('%d-%m-%Y H%H M%M S%S')) 
    path = ''.join([r'Regional Data ', dt_string, r'.pickle'])
    with open(path , 'wb') as f:
        pickle.dump(regional, f)


sg.theme('DarkAmber')

inputTab = [
            [
                sg.Table([['', '', '', '']], 
                headings=["Raw Data", "Defense Comments", "Catastrophe Comments", "Other Comments"],
                key="rawMatchList", expand_x=True, expand_y=True, auto_size_columns=True)
            ],
            [sg.Button("Input Data", key="input")]
           ]   

firstPickTab = [
                [sg.Table([['','']],  
                    headings=["Team Number", "Tele Avg. Points", "Auto Avg. Points", "Climb Level", "Percent High Plus"],
                    key="ShotThreshold", expand_y=True, auto_size_columns=True), 
                ]
               ]

tab3 = [
        [sg.Table([['', '', '', '', '']], 
            headings=["Team Number", "Tele Avg. Points", "Auto Avg. Points", "Normal Climb Level, Percent", "Percent High+ Climb"],
            key="masterTable", expand_x=False, expand_y=True, auto_size_columns=True)
        ]
       ]

tab4 = [
        [sg.Text("Enter Team Number"), sg.InputText(key="lookupKey")],
        [sg.Table([['', '', '', '', '']], 
            headings=["Tele Avg. Points", "Auto Avg. Points", "Normal Climb Level, Percent", "Percent High+ Climb"],
            key="lookupTable", expand_x=True, auto_size_columns=True)
        ]
       ]

tg_layout = [[
                sg.Tab('Input Data', inputTab, tooltip='tip'), 
                sg.Tab('First Pick', firstPickTab), 
                sg.Tab('Main List', tab3), 
                sg.Tab('Team Lookup', tab4)
            ]]

mainWindowLayout = [
                     [sg.TabGroup(tg_layout, expand_x=True, expand_y=True)],
                     [sg.Button("Save Data", key="save")]
                   ]

window = sg.Window("Main Window", mainWindowLayout, size=(800,500), resizable=True)

validDataEntry = False

def addMatch(data: tuple):
    if not data[0] == "":
        f = StringIO(data[0])
        dataList = list(csv.reader(f, delimiter=';'))[0]
        print(dataList)
    else:
        raise ValueError("No Match Data")

    mData = r.matchData(dataList)
    m = r.match(mData, data[1], data[2], data[3])
    regional.addNewMatch(m)
    regional.rawMatchList.append([m, data[1], data[2], data[3]])

def matchEntry():
    matchEntryLayout = [
        [sg.Text("Input Data and comments")],
        [sg.Text("Data"), sg.InputText()],
        [sg.Text("Defense Comments"), sg.InputText()],
        [sg.Text("Failure Comments"), sg.InputText()],
        [sg.Text("Other Comments"), sg.InputText()],
        [sg.Button("Submit")],
        ]
    
    meWin = sg.Window("Data Input", matchEntryLayout)
    
    while True:
        event, values = meWin.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Submit":
            data = values[0]
            defenseComments = values[1]
            failComments = values[2]
            otherComments = values[3]
            # append a match instance to the match list
            meWin.close()

            return data, defenseComments, failComments, otherComments

        if event == sg.WIN_CLOSED: 
            meWin.close()
            return "Closed_Before_Entry"

# File Selection Window
fswLayout = [
            [sg.Text("Choose a data file, or hit skip (if starting from scratch)")],
            [sg.InputText(key="file_name"), sg.FileBrowse()],
            [sg.Button("Submit"), sg.Button("Skip")],
        ]

fileSelectWindow = sg.Window("Select Data File", fswLayout)


while True: 
    event, values = fileSelectWindow.read()
    fileLocation = values

    print(fileLocation['Browse'])
    
    if event == "Submit":
        try:
            if os.path.exists(fileLocation['Browse']):
                f = open(fileLocation['Browse'], 'rb')
                regional = pickle.load(f)
                f.close()
                fileSelectWindow.close()
                break
            else:
                raise ValueError("No Such File Exists")

        except ValueError:
            e, v = sg.Window("Enter a valid file", [[sg.Text("The file you entered does not exist")],
                [sg.Button("Ok")]]).read(close=True)
            traceback.print_exc()

    if event == "Skip":
        fileSelectWindow.close()
        break

stime = time.time()
try:
    while True: 
        event, values = window.read(timeout=50) 

        if event == "input":
            entry = matchEntry()

            if not entry == "Closed_Before_Entry":
                try: 
                    addMatch(entry)

                except ValueError as e: 
                    print(e) 
                    print("Invalid Data Entry")
            else:
                print("No Entry")

        if event == "save":
            pickleRegional()
            
        if event == sg.WIN_CLOSED:
            pickleRegional()
            break
        
        regional.getTeamsOverTelePointThreshold(0, 20)
        regional.updateAutoData(20)
        regional.updateClimbData(20)

        firstPickList = list()

        t: r.team
        for t in regional.teamsOverShotThreshold:
            firstPickList.append([t.teamNumber, round(t.averageTelePoints,3), round(t.averageAutoPoints, 3), t.levels[0][0]+ '\t' +str(round(t.levels[0][2], 3)), t.high_plus_percent])
        
        firstPickList = firstPickList if len(firstPickList) >= 1 else [[ '', '', '', '']]

        if time.time() - stime >= (10*60):
            print("Data Saved")
            pickleRegional()
            stime = time.time()
        
        displayMatchList = list()
        for i in regional.rawMatchList:
            displayMatchList.append([str(i[0].data.mainList), i[1], i[2], i[3]])
        
        masterList_unsorted = list()
        t: r.team
        for key, t in regional.teamList.items():
            if t.teamNumber == '':
                continue

            teamNumber = int(t.teamNumber)
            masterList_unsorted.append([teamNumber, round(t.averageTelePoints, 3), round(t.averageAutoPoints, 3), t.levels[0][0]+ '\t' +str(round(t.levels[0][2], 3)), t.high_plus_percent])

        masterList = sorted(masterList_unsorted, key=lambda t: t[0])
        
        lookupNumber = values['lookupKey'] if values['lookupKey'] in regional.teamList.keys() else None
        if not lookupNumber == None:
            lookupTableList = [[round(regional.teamList[lookupNumber].averageTelePoints, 3), 
                                round(regional.teamList[lookupNumber].averageAutoPoints,3), 
                                t.levels[0][0]+ '\t' +str(round(t.levels[0][2], 3)), t.high_plus_percent]]
        else:
            lookupTableList = ['', '', '', '']

        window["masterTable"].Update(values=masterList)
        window["lookupTable"].Update(values=lookupTableList)
        window["ShotThreshold"].Update(values=firstPickList)
        #window["Auto"].Update()
        window["rawMatchList"].Update(values=displayMatchList)
        window.refresh()
except:
    traceback.print_exc()
    pickleRegional()
