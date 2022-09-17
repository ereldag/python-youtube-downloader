# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com


import PySimpleGUI as sg
from pytube import YouTube
from pytube import Playlist
import os

# ----------- download functions -----------


def download_song(song_url, file_name, file_path):
    try:
        yt = YouTube(song_url)
        print(yt.title, file_name, file_path)
        if file_name and file_path:
            yt.streams.get_audio_only().download(filename=file_name, output_path=file_path)
        elif file_name:
            yt.streams.get_audio_only().download(filename=file_name)
        elif file_path:
            yt.streams.get_audio_only().download(output_path=file_path)
        else:
            yt.streams.get_audio_only().download()
        return True
    except Exception as e:
        print(e.message)
        return False


def download_single_song(window, action, values):
    #print(action, values)
    url = values[f'-IN-{action}-URL-']
    file_name = values[f'-IN-{action}-name-']
    file_path = values[f'-IN-{action}-path-']

    if not os.path.exists(file_path):
        pass
        # TODO: add validation output
    if '.' in file_name:
        file_name = file_name

    output = window[f'-OUT-{action}-']
    status = download_song(url, file_name, file_path)
    if status:
        output.update(output.get()+'success!\n')
    else:
        output.update(output.get()+'failed...\n')


def download_csv_songs(window, action, values):
    pass


def download_playlist(window, action, values):
    pass


# ----------- functions to create the layouts this Window will display -----------


def create_single_song_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("youtube song URL:"), sg.InputText(
                  key=f'-IN-{action}-URL-')],
              [sg.Text("file name:"), sg.InputText(
                  key=f'-IN-{action}-name-')],
              [sg.Text("download location:"), sg.Text(), sg.FolderBrowse(
                  key=f'-IN-{action}-path-')],
              [sg.Submit(key=f'-SUB-{action}-')],
              [sg.ProgressBar(key=f'-PROG-{action}-', max_value=20)],
              [sg.Multiline(key=f'-OUT-{action}-',)]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


def create_csv_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("csv location:"), sg.Text(), sg.FileBrowse(
                  key=f'-IN-{action}-file-')],
              [sg.Submit()],
              [sg.ProgressBar(key=f'-PROG-{action}-', max_value=20)],
              [sg.Multiline(key=f'-OUT-{action}-',)]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


def create_playlist_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("youtube playlist URL:"),
               sg.InputText(key=f'-IN-{action}-url-')],
              [sg.Submit()],
              [sg.ProgressBar(key=f'-PROG-{action}-', max_value=20)],
              [sg.Multiline(key=f'-OUT-{action}-',)]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


def main():

    # set theme
    sg.theme("DarkBrown4")

    # ----------- Create layout using specified functions and index
    MENU = {"download single song": [create_single_song_layout, download_single_song],
            "download songs from csv": [create_csv_layout, download_csv_songs],
            "download playlist": [create_playlist_layout, download_playlist]}

    cols = []
    menu_btns = []
    for action, func in MENU.items():
        cols.append(func[0](action))
        menu_btns.append(sg.Button(action))

    # create window
    window = sg.Window('youtube downloader', [cols, menu_btns])

    # event loop
    current_action = ''  # The currently visible layout
    while True:
        event, values = window.read()
        print('\n---------------------------\n')
        print(event, values)

        # quit
        if event in (None, 'Exit'):
            break

        # switch layout upon button press
        if event in MENU.keys():
            if current_action != '':
                window[f'-COL-{current_action}-'].update(visible=False)
            current_action = event
            window[f'-COL-{current_action}-'].update(visible=True)

        # call current action download func
        elif event.find('-SUB-') != -1:

            MENU[current_action][1](window, current_action, values)

    window.close()


if __name__ == '__main__':
    main()
