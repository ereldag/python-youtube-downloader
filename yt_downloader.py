# Author: Erel Dagan, DevOps Engineer. ereldag18@gmail.com
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import argparse
import csv
import os

# Function to convert and dwonload youtube videos


def convert_download(url):
    driver.get("https://ytmp3.cc/en9/")
    url_input = driver.find_element_by_id('input')
    url_input.send_keys(url)
    convert_button = driver.find_element_by_id('submit')
    convert_button.click()
    time.sleep(1.5)
    download_button = driver.find_elements_by_link_text('Download')
    try:
        download_button = download_button[0]
    except:
        time.sleep(20)
        download_button = driver.find_elements_by_link_text('Download')
        download_button = download_button[0]
    download_button.click()
    time.sleep(2)


chromedriver = r"{}\chromedriver.exe".format(
    os.path.dirname(os.path.realpath(__file__)))
downloads_path = r"{}\downloads".format(
    os.path.dirname(os.path.realpath(__file__)))

# Arguments Parser
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', dest='url',
                    help="url from youtube to be Downloaded")
parser.add_argument('-b', '--bin-location', dest='bin', help="Path for the .exe file of chrome",
                    default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
parser.add_argument('-f', '--csv-file', dest='csv',
                    help="Path for csv file wirh urls to be downloaded")
parser.add_argument('-c', '--chrome-driver', dest='chromedriver',
                    help="Path to chrome driver location", default=chromedriver)
parser.add_argument('-d', '--download-path', dest='downloads_path',
                    help="Path for files to be dowloaded to", default=downloads_path)
args = parser.parse_args()

# Arguments validation
if not args.csv and not args.url:
    raise parser.error('Must Enter url or csv path')
elif args.csv and args.url:
    raise parser.error('Enter url OR csv path')

if not os.path.exists(downloads_path):
    os.mkdir(downloads_path)

# Creates the chrome driver with custom options
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": args.downloads_path}
options.add_experimental_option("prefs", prefs)
options.binary_location = args.bin
driver = webdriver.Chrome(options=options, executable_path=args.chromedriver, )

# Check if csv path was entered
if args.csv:
    with open(f'{args.csv}', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for url in reader:
            convert_download(url)
            print(f"Succesfully downloaded {url}!")
elif args.url:
    convert_download(args.url)
    print(f"Succesfully downloaded {args.url}!")

driver.quit()
