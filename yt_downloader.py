# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com

from csv import reader
import PySimpleGUI as sg
from pytube import YouTube
from pytube import Playlist
import os
import threading
import sys
# ----------- download functions -----------


def write_output(output, lock, message="", newlines=1):
    lock.acquire()
    output.print(message+('\n'*newlines))
    lock.release()


# update progress bar
def update_progress_bar(pb, text, lock, finished, count):
    lock.acquire()

    # calculate percentage of completed songs
    percent = round((finished/count)*100)
    pb.update(percent)
    text.update(f"finished {finished} out of {count}")

    lock.release()


def download_song(output, lock, url, file_path, file_name=""):
    if file_path == "":
        file_path = os.getcwd()
    if not os.path.exists(file_path):
        write_output(output, lock, 'failed - path not found!')
        # TODO: add validation output
    else:
        try:
            yt = YouTube(url)

            # give title to files with no name, and append .mp3 to file names without type
            if file_name == "":
                file_name = yt.title + ".mp3"
            elif '.' not in file_name:
                file_name = file_name + ".mp3"

            # write output to gui
            write_output(
                output, lock, f'downloading {yt.title} as {file_path}\\{file_name} ')

            # download
            yt.streams.get_audio_only().download(filename=file_name, output_path=file_path)

            # write success to gui
            write_output(output, lock, 'success!', newlines=2)

        except Exception as e:

            # write exception to gui
            write_output(output, lock, 'failed... view error message below')
            write_output(output, lock, f'{e.args}', newlines=2)


def download_single_song(window, action, values, lock):
    url = values[f'-IN-{action}-URL-']
    file_name = values[f'-IN-{action}-name-']
    file_path = values[f'-IN-{action}-path-']
    output = window[f'-OUT-{action}-']

    # download song
    download_song(output, lock, url, file_path, file_name)
    write_output(output, lock, newlines=2)


def download_csv_songs(window, action, values, lock):
    csv_path = values[f'-IN-{action}-file-']
    output = window[f'-OUT-{action}-']

    pb = window[f"-PROG-{action}-"]
    pb_text = window[f"-PROG-TEXT-{action}-"]

    with open(csv_path, newline='') as csv:
        count = sum(1 for line in csv)

    finished = 0

    update_progress_bar(pb, pb_text, lock, finished, count)

    write_output(output, lock, f'reading csv {csv_path}...')
    # read csv and download specified songs
    with open(csv_path, newline='') as csv:
        for line in reader(csv):
            file_name = line[0].replace('\t', '')
            file_path = line[1]
            url = line[2]
            download_song(output, lock, url, file_path, file_name)

            finished += 1
            update_progress_bar(pb, pb_text, lock, finished, count)

    write_output(output, lock, f'finished reading {csv_path}!', newlines=2)


def download_playlist(window, action, values, lock):
    url = values[f'-IN-{action}-url-']
    output = window[f'-OUT-{action}-']
    file_path = values[f'-IN-{action}-path-']

    # create playlist and download each song inside
    plist = Playlist(url)

    pb = window[f"-PROG-{action}-"]
    pb_text = window[f"-PROG-TEXT-{action}-"]

    count = plist.length
    finished = 0
    write_output(output, lock, f'downloading playlist {plist.title}')
    update_progress_bar(pb, pb_text, lock, finished, count)

    for url in plist.video_urls:
        download_song(output, lock, url, file_path=file_path)
        finished += 1
        update_progress_bar(pb, pb_text, lock, finished, count)

    write_output(
        output, lock, f'finished downloading playlist {plist.title}!', newlines=2)

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
              [sg.Multiline(key=f'-OUT-{action}-', size=(50, 10))]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


# layout for csv
def create_csv_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("csv location:"), sg.Text(), sg.FileBrowse(
                  key=f'-IN-{action}-file-', file_types=(("comma seperated values", "*.csv"),),)],
              [sg.Submit(key=f'-SUB-{action}-')],
              [sg.ProgressBar(key=f'-PROG-{action}-', max_value=100,
                              size=(30, 15)), sg.Text(key=f"-PROG-TEXT-{action}-")],
              [sg.Multiline(key=f'-OUT-{action}-', size=(70, 10), autoscroll=True)]]
    return sg.Column(layout, key=f'-COL-{action}-', visible=False)


# layout for playlist
def create_playlist_layout(action):
    layout = [[sg.Text(action)],
              [sg.Text("youtube playlist URL:"),
               sg.InputText(key=f'-IN-{action}-url-')],
              [sg.Text("download location:"), sg.Text(), sg.FolderBrowse(
                  key=f'-IN-{action}-path-')],
              [sg.Submit(key=f'-SUB-{action}-')],
              [sg.ProgressBar(key=f'-PROG-{action}-', max_value=100,
                              size=(30, 15)), sg.Text(key=f"-PROG-TEXT-{action}-")],
              [sg.Multiline(key=f'-OUT-{action}-', size=(70, 10), autoscroll=True)]]
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

    # add icon path after pyinstaller conversion
    try:
        icon_path = sys._MEIPASS + '\icons\logo.ico'
    except:
        icon_path = r'icons/logo.ico'

    # create window
    window = sg.Window('youtube downloader', [
                       cols, menu_btns], icon=icon_path)

    # create thread lock
    lock = threading.Lock()

    # event loop
    current_action = ''  # The currently visible layout
    while True:
        event, values = window.read()

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
