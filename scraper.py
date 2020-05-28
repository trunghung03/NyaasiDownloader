import bs4
import requests
import os
import re
import webbrowser
import time
import sys
import argparse

from getpass import getuser


def checklink(links, no1, no3):  
    torrent_name = no3
    folder = no1
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


def check_sukebei(no2):
    if no2 == "0":
        return 'https://nyaa.si'
    else:
        return 'https://sukebei.nyaa.si'


def make_link(no4, no2):
    link = '{}/user/{}'.format(check_sukebei(no2), no4)
    return bs4.BeautifulSoup(requests.get(link).text, features='html.parser')


def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('--l', type=str, default="/home/{}/Downloads/FAKKU/".format(getuser()), 
                        help="Name location that you want to check for existing files.")
    parser.add_argument('--s', type=str, default="1", 
                        help="0 for vanilla; 1 for sukebei.")
    parser.add_argument('--n', type=str, default="fakku", 
                        help="Name of torrents you want to download.")
    parser.add_argument('--u', type=str, default="rbot2000", 
                        help="Name of user.")
    args = parser.parse_args()

    url = check_sukebei(args.s)
    prelink = make_link(args.u, args.s)
    soup = [a for a in prelink.select('tbody > tr')]
    filter = checklink(prelink.select('tbody > tr > td > a'), args.l, args.n)
    precum = [link.find('a', href=re.compile('^/download/')) for link in listmaker(soup, filter)]
    links = [item.get('href') for item in precum]
    for download in links:
        webbrowser.open(url + download)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
# example
# $ python3 scraper.py --l ~/Downloads/FAKKU/ --s 1 --n fakku --u rbot2000 
# will download every fakku torrent from user rbot2000