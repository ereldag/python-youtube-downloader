# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com

import PySimpleGUI as sg
from pytube import YouTube
from pytube import Playlist
import os


# set theme
sg.theme("DarkBrown4")

# ----------- Create the 3 layouts this Window will display -----------


def create_single_song_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("youtube song URL:"), sg.InputText(
                  key=f'-IN-{action}-')],
              [sg.Submit(key=f'-SUB-{action}-')]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


def create_csv_layout(action):
    layout = [[sg.Text(action)],
              [sg.Input(key=f'-IN-{action}-')],
              [sg.Input(key=f'-IN2-{action}-')]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


def create_playlist_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("youtube playlist URL:"),
               sg.InputText(key=f'-IN-{action}-')],
              [sg.Submit()]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


# ----------- Create actual layout using Columns and a row of Buttons
MENU = {"download single song": create_single_song_layout,
        "download songs from csv": create_csv_layout, "download playlist": create_playlist_layout}

cols = []
menu_btns = []
for action, create_col in MENU.items():
    cols.append(create_col(action))
    menu_btns.append(sg.Button(action))

window = sg.Window('Swapping the contents of a window', [cols, menu_btns])


# event loop
cur_layout = ''  # The currently visible layout
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event in MENU.keys():
        if cur_layout != '':
            window[f'-COL-{cur_layout}-'].update(visible=False)
        cur_layout = event
        window[f'-COL-{cur_layout}-'].update(visible=True)
window.close()
