from models import db, Stations, Schedule
from lxml import html
import requests
import sys
import HTMLParser
import re

# Request all stations, parse into html tree
stations_page = requests.get('http://m.njtransit.com/mo/mo_servlet.srv?hdnPageAction=DvTo')
stations_tree = html.document_fromstring(stations_page.text)

# Get new version number for upcoming iteration of scraping all stations data
version = db.session.query(db.func.max(Stations.version)).scalar()
if version == None:
	version = 0

version = version + 1

html_parser = HTMLParser.HTMLParser()

# For each station
for val in stations_tree.xpath('//option'):
	if(len(val.attrib['value'])):

		# Create new stations
		station = Stations(val.text, val.attrib['value'], version)

		# Request page with all schedule data for that station
		trains_page = requests.get('http://dv.njtransit.com/mobile/tid-mobile.aspx?sid=' + val.attrib['value'])
		trains_tree = html.document_fromstring(trains_page.text)

		# Scrape stations
		for elem in trains_tree.xpath('//table'):
			if len(elem.getchildren()) == 1 and len(elem.getchildren()[0].getchildren()) == 6:
				values = [re.sub('[^a-zA-Z0-9- :_*.]', '', x.text_content().strip()) for x in (elem.getchildren()[0].getchildren())]
				schedule = Schedule(values[0], values[1], values[2], values[3], values[4], values[5])
				db.session.add(schedule)
				db.session.commit()
				print values
				print "--"

		print trains_page.status_code

		db.session.add(station)
		db.session.commit()

#		sys.exit(0)

