# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com

from csv import reader
import PySimpleGUI as sg
from pytube import YouTube
from pytube import Playlist
import os
import threading

# ----------- download functions -----------


def write_output(output, lock, message):
    lock.acquire()
    output.update(output.get()+'\n'+message)
    lock.release()


# change progress bar on download progress
def update_progress_Bar(self, file_handle, bytes_remaining):
    print(bytes_remaining)


# update stuff on completion
def complete_progress_bar(stream, file_handle):
    pass


def download_song(output, lock, url, file_path, file_name=""):
    if file_path == "":
        file_path = os.getcwd()
    if not os.path.exists(file_path):
        write_output(output, lock, 'failed - path not found!')
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
            write_output(
                output, lock, f'downloading {yt.title} as {file_path}\\{file_name} ')
            print(yt.title, file_name, file_path)

            # download
            yt.streams.get_audio_only().download(filename=file_name, output_path=file_path)

            # write success to gui
            write_output(output, lock, 'success!')

        except Exception as e:

            # write exception to gui
            write_output(output, lock, 'failed... view error message below')
            write_output(output, lock, f'{e.args}')


def download_single_song(window, action, values, lock):
    url = values[f'-IN-{action}-URL-']
    file_name = values[f'-IN-{action}-name-']
    file_path = values[f'-IN-{action}-path-']
    output = window[f'-OUT-{action}-']

    # download song
    download_song(output, lock, url, file_path, file_name)


def download_csv_songs(window, action, values, lock):
    csv_path = values[f'-IN-{action}-file-']
    output = window[f'-OUT-{action}-']

    write_output(output, lock, f'reading csv {csv_path}...')

    # read csv and download specified songs
    with open(csv_path, newline='') as csv:
        for line in reader(csv):
            file_name = line[0].replace('\t', '')
            file_path = line[1]
            url = line[2]
            download_song(output, lock, url, file_path, file_name)

    write_output(output, lock, f'finished reading {csv_path}')


def download_playlist(window, action, values, lock):
    url = values[f'-IN-{action}-url-']
    output = window[f'-OUT-{action}-']
    file_path = values[f'-IN-{action}-path-']

    # create playlist and download each song inside
    plist = Playlist(url)

    write_output(output, lock, f'downloading playlist {plist.title}')

    for url in plist.video_urls:
        download_song(output, lock, url, file_path=file_path)

    write_output(output, lock, f'finished downloading playlist {plist.title}')


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
              [sg.Multiline(key=f'-OUT-{action}-', size=(50, 10))]]
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
              [sg.Multiline(key=f'-OUT-{action}-', size=(50, 10))]]
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
    window = sg.Window('youtube downloader', [
                       cols, menu_btns], icon=r'icons/logo.ico')

    # create thread lock
    lock = threading.Lock()

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
            threading.Thread(target=MENU[current_action][1], args=(
                window, current_action, values, lock)).start()

    window.close()


# --------------------------------------------------------------------------

if __name__ == '__main__':
    main()
