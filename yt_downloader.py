# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com

import PySimpleGUI as sg
from pytube import YouTube
from pytube import Playlist
import os


# set theme
sg.theme("DarkBrown4")

# ----------- Create the 3 layouts this Window will display -----------
single_file_layout = [[sg.Text('download single song')],
                      [sg.Text("youtube song URL:"), sg.InputText(
                          key='-IN-single-song-url')],
                      [sg.Submit(key='-SUB-download single song-')]]

multiple_from_csv_layout = [[sg.Text('download all songs from csv')],
                            [sg.Input(key='-IN-')],
                            [sg.Input(key='-IN2-')]]

playlist_layout = [[sg.Text('download all songs in playlist')],
                   [sg.Text("youtube playlist URL:"),
                    sg.InputText(key='-IN-playlist-url')],
                   [sg.Submit()]]

# ----------- Create actual layout using Columns and a row of Buttons
MENU = {"download single song": single_file_layout,
        "download songs from csv": multiple_from_csv_layout, "download playlist": playlist_layout}

cols = []
menu_btns = []
for action, layout in MENU.items():
    cols.append(sg.Column(layout, key=f'-COL-{action}-', visible=False))
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
