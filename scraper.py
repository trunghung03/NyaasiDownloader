# download fakku torrent from user rbot2000

import bs4
import requests
import os
import re
import webbrowser
import time
import sys


def checklink(links):  # check for torrents that you want to get
    linkslist = []
    for link in links:
        text = link.getText().lower()
        if not text.startswith(torrent_name) or os.path.isdir(folder + text):
            # change this part if you want to download a series from another user
            continue
        linkslist.append(link)
    return linkslist


def resultsetlist(resultset):  # convert resultset to list
    resultlist = []
    for result in resultset:
        resultlist.append(result)
    return resultlist


def listmaker(linkslist, filterlist):  # add items that isn't in directory yet to list of downloads
    finallist = []
    for link in linkslist:
        for filt in filterlist:
            if str(filt) in str(link):
                finallist.append(link)
    return finallist


def findthelinks(dalist):  # find all download link from final list
    dalinks = []
    for dal in dalist:
        for item in dal.find_all('a', href=re.compile('^/download/')):
            item = item.get('href')
            dalinks.append(item)
    return dalinks


def downloaddalist(downloadlist):  # download the torrent
    for download in downloadlist:
        webbrowser.open(url + download)
        time.sleep(1)


def check_sukebei(number):
    if number == 0:
        return 'https://nyaa.si'
    else:
        return 'https://sukebei.nyaa.si'


folder = sys.argv[1]
# folder to check for duplicates 
url = check_sukebei(int(sys.argv[2])) # 0 for vanilla and 1 for sukebei
torrent_name = sys.argv[3]
user_name = sys.argv[4]
fakkuHTML = requests.get('{}/user/{}'.format(url, user_name))
fakkuHTML.raise_for_status()
fakkuSoup = bs4.BeautifulSoup(fakkuHTML.text, features='lxml')
fakkuLinks = fakkuSoup.select('tbody > tr > td > a')



fakku = checklink(fakkuLinks)
finalList = listmaker(resultsetlist(fakkuSoup.select('tbody > tr')), fakku)
downloaddalist(findthelinks(finalList))
