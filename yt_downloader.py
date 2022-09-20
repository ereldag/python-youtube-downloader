# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com

from csv import reader
import PySimpleGUI as sg
from pytube import YouTube
from pytube import Playlist
import os

# ----------- download functions -----------


# change progress bar on download progress
def update_progress_Bar(self, file_handle, bytes_remaining):
    print(bytes_remaining)


# update stuff on completion
def complete_progress_bar(stream, file_handle):
    pass


def download_song(url, file_name="", file_path=os.getcwd(), output=""):

    if not os.path.exists(file_path):
        output.update(output.get()+'\n'+'failed - path not found!')
        # TODO: add validation output
    else:
        try:
            yt = YouTube(url, on_progress_callback=update_progress_Bar,
                         on_complete_callback=complete_progress_bar)

            # give title to files with no name, and append .mp3 to file names without type
            if file_name == "":
                file_name = yt.title + ".mp3"
            elif '.' not in file_name:
                file_name = file_name + ".mp3"

            # write output to gui
            output.update(
                output.get()+'\n'+f'downloading {yt.title} as {file_path}\\{file_name} ')
            print(yt.title, file_name, file_path)

            # download
            yt.streams.get_audio_only().download(filename=file_name, output_path=file_path)

            # write success to gui
            output.update(output.get()+'\n'+'success!')

        except Exception as e:

            # write exception to gui
            output.update(output.get()+'\n' +
                          'failed... view error message below')
            output.update(output.get()+'\n'+f'{e.args}')


def download_single_song(window, action, values):
    #print(action, values)
    url = values[f'-IN-{action}-URL-']
    file_name = values[f'-IN-{action}-name-']
    file_path = values[f'-IN-{action}-path-']
    output = window[f'-OUT-{action}-']

    # download song
    download_song(url, file_name, file_path, output)


def download_csv_songs(window, action, values):
    csv_path = values[f'-IN-{action}-file-']
    output = window[f'-OUT-{action}-']

    output.update(output.get()+'\n'+f'reading csv {csv_path}...')

    # read csv and download specified songs
    with open(csv_path, newline='') as csv:
        for line in reader(csv):
            file_name = line[0].replace('\t', '')
            file_path = line[1]
            url = line[2]
            download_song(url, file_name, file_path, output)

    output.update(output.get()+'\n'+f'finished reading {csv_path}')


def download_playlist(window, action, values):
    url = values[f'-IN-{action}-url-']
    output = window[f'-OUT-{action}-']
    file_path = values[f'-IN-{action}-path-']

    # create playlist and download each song inside
    plist = Playlist(url)

    for url in plist.video_urls:
        download_song(url, file_path=file_path, output=output)


# ----------- functions to create the layouts this Window will display -----------


# layout for single song
def create_single_song_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("youtube song URL:"), sg.InputText(
                  key=f'-IN-{action}-URL-')],
              [sg.Text("file name:"), sg.InputText(
                  key=f'-IN-{action}-name-')],
              [sg.Text("download location:"), sg.Text(), sg.FolderBrowse(
                  key=f'-IN-{action}-path-')],
              [sg.Submit(key=f'-SUB-{action}-')],
              [sg.ProgressBar(key=f'-PROG-{action}-', max_value=100)],
              [sg.Multiline(key=f'-OUT-{action}-', size=(50, 10))]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


# layout for csv
def create_csv_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("csv location:"), sg.Text(), sg.FileBrowse(
                  key=f'-IN-{action}-file-', file_types=(("comma seperated values", "*.csv"),),)],
              [sg.Submit(key=f'-SUB-{action}-')],
              [sg.ProgressBar(key=f'-PROG-{action}-', max_value=100)],
              [sg.Multiline(key=f'-OUT-{action}-',)]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


# layout for playlist
def create_playlist_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("youtube playlist URL:"),
               sg.InputText(key=f'-IN-{action}-url-')],
              [sg.Text("download location:"), sg.Text(), sg.FolderBrowse(
                  key=f'-IN-{action}-path-')],
              [sg.Submit(key=f'-SUB-{action}-')],
              [sg.ProgressBar(key=f'-PROG-{action}-', max_value=100)],
              [sg.Multiline(key=f'-OUT-{action}-',)]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


# --------------------------------------------------------------------------------

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


# --------------------------------------------------------------------------

if __name__ == '__main__':
    main()
