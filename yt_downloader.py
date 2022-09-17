# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com

import PySimpleGUI as sg
from pytube import YouTube
from pytube import Playlist
import os

# ----------- Create the 3 layouts this Window will display -----------
single_file_layout = [[sg.Text('download single song')],
                      *[[sg.CB(f'Checkbox {i}')] for i in range(5)]]

multiple_from_csv_layout = [[sg.Text('download all songs from csv')],
                            [sg.Input(key='-IN-')],
                            [sg.Input(key='-IN2-')]]

playlist_layout = [[sg.Text('download all songs in playlist')],
                   *[[sg.R(f'Radio {i}', 1)] for i in range(8)]]

# ----------- Create actual layout using Columns and a row of Buttons
MENU_ACTIONS = {"download single song": single_file_layout,
                "download songs from csv": multiple_from_csv_layout, "download playlist": playlist_layout}

cols = []
menu = []
for action, layout in MENU_ACTIONS.items():
    cols.append(sg.Column(layout, key=f'-col-{action}', visible=False))
    menu.append(sg.Button(action))

window = sg.Window('Swapping the contents of a window', [cols, menu])


# event loop
cur_layout = ''  # The currently visible layout
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event in MENU_ACTIONS.keys():
        window[f'-COL{cur_layout}-'].update(visible=False)
        cur_layout = int(event)
        window[f'-COL{cur_layout}-'].update(visible=True)
window.close()
