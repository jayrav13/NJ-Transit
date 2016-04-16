from models import db, Stations, Schedule, Requests
from lxml import html
import requests
import sys
import HTMLParser
import re
import time
import os

# Request all stations, parse into html tree
stations_page = requests.get('http://m.njtransit.com/mo/mo_servlet.srv?hdnPageAction=DvTo')
stations_tree = html.document_fromstring(stations_page.text)

for val in stations_tree.xpath('//option'):
	station = Stations.query.filter_by(abbr=val.attrib['value']).first()
	if not station and val.attrib['value']:
		db.session.add(Stations(val.text, val.attrib['value']))
		db.session.commit()

html_parser = HTMLParser.HTMLParser()

# Get new version number for upcoming iteration of scraping all stations data
version = db.session.query(db.func.max(Requests.version)).scalar()
if version == None:
	version = 0

version = version + 1

# For each station
for station in Stations.query.all():

		# Request page with all schedule data for that station
		url = 'http://dv.njtransit.com/mobile/tid-mobile.aspx?sid=' + station.abbr
		request_time = time.time()
		trains_page = requests.get(url)
		request_time = time.time() - request_time
		trains_tree = html.document_fromstring(trains_page.text)

		# Scrape stations
		for elem in trains_tree.xpath('//table'):
			if len(elem.getchildren()) == 1 and len(elem.getchildren()[0].getchildren()) == 6:
				values = [re.sub('[^a-zA-Z0-9- :_*.]', '', x.text_content().strip()) for x in (elem.getchildren()[0].getchildren())]
				schedule = Schedule(values[0], values[1], values[2], values[3], values[4], values[5])
				station.schedules.append(schedule)
				print values
	
		db.session.add(Requests(url, request_time, version))

db.session.commit()



print "Success."
