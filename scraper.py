#download fakku torrent from user rbot2000

import bs4
import requests
import os
import re
import webbrowser
import time


fakkuHTML = requests.get('https://sukebei.nyaa.si/user/rbot2000')
fakkuHTML.raise_for_status()
fakkuSoup = bs4.BeautifulSoup(fakkuHTML.text, features='lxml')
fakkuLinks = fakkuSoup.select("tbody > tr > td > a")


def checklink(links): # find list of fakku torrent that haven't been downloaded yet
	linkslist = []
	for link in links:
		text = link.getText().lower()
		if not text.startswith("fakku") or os.path.isdir('/home/synapse26/Downloads/FAKKU/' + text):
			continue
		linkslist.append(link)
	return linkslist


def resultsetlist(resultset): # convert from resultset to list
	resultlist = []
	for set in resultset:
		resultlist.append(set)
	return resultlist


def listmaker(linkslist, filterlist): # check if item exist in list[index] yet, if not then append to final list
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


def downloaddalist(downloadlist): # download the fucking torrent
	for download in downloadlist:
		webbrowser.open('https://sukebei.nyaa.si' + download)
		time.sleep(1)


fakku = checklink(fakkuLinks)
finalList = listmaker(resultsetlist(fakkuSoup.select("tbody > tr")), fakku)
downloaddalist(findthelinks(finalList))