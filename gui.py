import PySimpleGUI as sg
import csv
import pickle
import os
import datetime as d
from datetime import datetime
from io import StringIO
import regional as r

PST_timezone = d.timezone(d.timedelta(hours=-8))
regional = r.regional()

def loadRegional(file):
    with open(file, 'rb') as f:
        regional = pickle.load(f)

def pickleRegional():
    with open(".\\pickled_data\\regionalData"+ datetime.now(tz=PST_timezone) +".pickle", 'wb') as f:
        pickle.dump(regional, f)


sg.theme('DarkAmber')

enteredDataList = [
    [sg.Table([["list"],[2]], expand_x=True, expand_y=True)]
    ]

inputTab = [
        [sg.Table()],
        [sg.Button("Input Data", key="input")]
        ]   

firstPickTab = [[sg.T('This is inside tab 2')],    
                       [sg.In(key='in')]]

tg_layout = [[sg.Tab('Input Data', inputTab, tooltip='tip'), sg.Tab('Tab 2', firstPickTab)]]

mainWindowLayout = [
        [sg.TabGroup(tg_layout, tooltip='TIP2')],
        ]

mainWindowLayout = [
        [sg.TabGroup(tg_layout, key="")]
        ]

window = sg.Window("Main Window", mainWindowLayout, size=(800,500), resizable=True)

def addMatch(data: tuple):
    if not data[0] == "":
        f = StringIO(data[0])
        dataList = list(csv.reader(f, delimiter=';'))[0]

    m = r.matchData(dataList)
    regional.addNewMatch(m, data[1], data[2], data[3])
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


while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "input":
        addMatch(matchEntry())
        
    if event == sg.WIN_CLOSED:
        pickleRegional()
        break 
