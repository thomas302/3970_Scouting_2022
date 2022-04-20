import PySimpleGUI as sg
import fileinput as fi
import csv
import pickle
import os
import datetime as d
import traceback
import regional as r

from datetime import datetime
from io import StringIO

PST_timezone = d.timezone(d.timedelta(hours=-8))
regional = r.regional()

def pickleRegional():
    dt = datetime.now()
    dt_string = r''.join(dt.strftime('%d-%m-%Y H%H M%M S%S'))
    path = r''.join([r'Regional Data ', dt_string, r'.pickle'])
    with open(path , 'wb') as f:
        pickle.dump(regional, f)


sg.theme('DarkAmber')

inputTab = [
        [sg.Table([['', '', '', '']], headings=["Raw Data", "Defense Comments", "Catastrophe Comments", "Other Comments"], key="rawMatchList", expand_x=True, expand_y=True)],
        [sg.Button("Input Data", key="input")]
        ]   

firstPickTab = [
            [sg.Table([['','']], headings=["Team Number", "Avg. Points"],key="ShotThreshold")],    
            ]

tg_layout = [[sg.Tab('Input Data', inputTab, tooltip='tip'), sg.Tab('Tab 2', firstPickTab)]]

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

    while True:
        meWin = sg.Window("Data Input", matchEntryLayout)
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


try:
    while True: 
        event, values = window.read(timeout=50) 

        if event == "input":
            entry = matchEntry()

            validDataEntry = True
            if not len(entry[0].split(";")) == 15:
                validDataEntry == False

            if validDataEntry:
                try: addMatch(entry)
                except ValueError as e: 
                    print(e) 
                    print("Invalid Data Entry")

        if event == "save":
            pickleRegional()
            
        if event == sg.WIN_CLOSED:
            pickleRegional()
            break

        
        regional.getTeamsOverTelePointThreshold(20)
        shotThresholdList = list()
        t: r.team
        for t in regional.teamsOverShotThreshold:
            shotThresholdList.append([t.teamNumber, t.averageTelePoints])
        
        shotThresholdList = shotThresholdList if len(shotThresholdList) >= 1 else ['','']

        window["ShotThreshold"].Update(values=shotThresholdList)
        window["rawMatchList"].Update(values=regional.rawMatchList)
        window.refresh()
except:
    traceback.print_exc()
    pickleRegional()
