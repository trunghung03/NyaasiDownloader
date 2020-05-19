import bs4
import requests
import os
import re
import webbrowser
import time

def checklink(links, number1, number3):  
    torrent_name = number3
    folder = number1
    alist = []
    for link in links:
        text = link.getText().lower()
        if not text.startswith(torrent_name) or os.path.isdir(folder + text):
            continue
        alist.append(link)
    return alist


def listmaker(linkslist, filter):
    alist = []
    for link in linkslist:
        for filt in filter:
            if str(filt) in str(link):
                alist.append(link)
    return alist


def check_sukebei(number2):
    if int(number2) == 0:
        return 'https://nyaa.si'
    else:
        return 'https://sukebei.nyaa.si'


def make_link(number4, number2):
    link = '{}/user/{}'.format(check_sukebei(number2), number4)
    return bs4.BeautifulSoup(requests.get(link).text, features='lxml')


def download(number1, number2, number3, number4): 
    url = check_sukebei(number2)
    prelink = make_link(number4, number2)
    soup = [a for a in prelink.select('tbody > tr')]
    filter = checklink(prelink.select('tbody > tr > td > a'), number1, number3)
    precum = [link.find('a', href=re.compile('^/download/')) for link in listmaker(soup, filter)]
    links = [item.get('href') for item in precum]
    for download in links:
        webbrowser.open(url + download)
        time.sleep(0.5)