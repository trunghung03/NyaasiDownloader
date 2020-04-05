#download fakku torrent from user rbot2000

import bs4
import requests
import os
import re
import webbrowser
import time


folder = '/home/synapse26/Downloads/FAKKU/'  # change this folder to your destination folder to check for duplicates
torrent_name = 'fakku' # change this to your wanted torrent to check for duplicates
url = 'https://sukebei.nyaa.si' # use 'https://nyaa.si' if you prefer the vanilla
fakkuHTML = requests.get(url + '/user/rbot2000') # change this part if you want to download from another user
fakkuHTML.raise_for_status()
fakkuSoup = bs4.BeautifulSoup(fakkuHTML.text, features='lxml')
fakkuLinks = fakkuSoup.select('tbody > tr > td > a')


def checklink(links): # check for torrents that you want to get
	linkslist = []
	for link in links:
		text = link.getText().lower()
		if not text.startswith(torrent_name) or os.path.isdir(folder + text):
		# change this part if you want to download a series from another user
			continue
		linkslist.append(link)
	return linkslist


def resultsetlist(resultset): # convert resultset to list
	resultlist = []
	for set in resultset:
		resultlist.append(set)
	return resultlist


def listmaker(linkslist, filterlist): # add items that isn't in directory yet to list of downloads
	finallist = []
	for link in linkslist:
		for filt in filterlist:
			if str(filt) in str(link):
				finallist.append(link)
	return finallist


def findthelinks(dalist): # find all download link from final list
	dalinks = []
	for dal in dalist:
		for item in dal.find_all('a', href=re.compile('^/download/')):
			item = item.get('href')
			dalinks.append(item)
	return dalinks


def downloaddalist(downloadlist): # download the torrent
	for download in downloadlist:
		webbrowser.open(url + download)
		time.sleep(1)


fakku = checklink(fakkuLinks)
finalList = listmaker(resultsetlist(fakkuSoup.select('tbody > tr')), fakku)
downloaddalist(findthelinks(finalList))
