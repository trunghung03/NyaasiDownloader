import bs4
import requests
import os
import re
import webbrowser
import time
import sys


def checklink(links):  # check for torrents that you want to get
    alist = []
    for link in links:
        text = link.getText().lower()
        if not text.startswith(torrent_name) or os.path.isdir(folder + text):
            continue
        alist.append(link)
    return alist


def listmaker(linkslist, filter):  # add items that isn't in directory yet to list of downloads
    alist = []
    for link in linkslist:
        for filt in filter:
            if str(filt) in str(link):
                alist.append(link)
    return alist


def downloaddalist(downloadlist):  # download the torrent
    for download in downloadlist:
        webbrowser.open(url + download)
        time.sleep(0.5)


def check_sukebei(number):
    if number == 0:
        return 'https://nyaa.si'
    else:
        return 'https://sukebei.nyaa.si'


folder = sys.argv[1]
url = check_sukebei(int(sys.argv[2]))
torrent_name = sys.argv[3]
user_name = sys.argv[4]
fakkuRawList = []


fakkuHTML = requests.get('{}/user/{}'.format(url, user_name))
fakkuHTML.raise_for_status()
fakkuSoup = bs4.BeautifulSoup(fakkuHTML.text, features='lxml')
fakkuLinks = fakkuSoup.select('tbody > tr > td > a')
fakku = checklink(fakkuLinks)
fakkuList = listmaker([a for a in fakkuSoup.select('tbody > tr')], fakku)
downloaddalist([item.get('href') for item in [link.find('a', href=re.compile('^/download/')) for link in fakkuList]])
# example
# $ python3 scraper.py ~/Downloads/FAKKU/ 1 fakku rbot2000 
# will download every fakku torrent from user rbot2000