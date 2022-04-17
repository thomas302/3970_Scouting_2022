import PySimpleGUI as sg
import csv
from io import StringIO
import regional as r

regional = r.regional()

sg.theme('DarkAmber')

inputFrameLayout = [
    [sg.Table([["list"],[2]], expand_x=True, expand_y=True)]
    ]

sg.TabGroup()

mainWindowLayout = [
        [sg.Frame("teamDataStuff", inputFrameLayout, expand_x=True, expand_y=True)],
        [sg.Button("Input Data")]
        ]

window = sg.Window("Main Window", mainWindowLayout, size=(800,500), resizable=True)

def addMatch(data: tuple):
    if not data[0] == "":
        f = StringIO(data[0])
        dataList = list(csv.reader(f, delimiter=';'))[0]

    m = r.matchData(dataList)
    regional.addNewMatch(m, data[1], data[2], data[3])


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
    if event == "Input Data":
        addMatch(matchEntry())
        
    if event == sg.WIN_CLOSED:
        break

import csv
from io import StringIO
import regional as r

sg.theme('DarkAmber')

inputFrameLayout = [
    [sg.Table([["list"],[2]], expand_x=True, expand_y=True)]
    ]

mainWindowLayout = [
        [sg.Frame("teamDataStuff",inputFrameLayout, expand_x=True, expand_y=True)],
        [sg.Button("Input Data")]
        ]

window = sg.Window("Main Window", mainWindowLayout, size=(800,500), resizable=True)

def addMatch(data: tuple):
    if not data[0] == "":
        f = StringIO(data[0])
        dataList = list(csv.reader(f, delimiter=';'))[0]





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
    if event == "Input Data":
        addMatch(matchEntry())
        
    if event == sg.WIN_CLOSED:
        break

