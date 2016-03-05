from models import db, Stations, Schedule, Requests
from lxml import html
import requests
import sys
import HTMLParser
import re
import time

time.sleep(0.01)

for i in range(0, 10):
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
			url = 'http://dv.njtransit.com/mobile/tid-mobile.aspx?sid=' + val.attrib['value']
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
					#db.session.add(schedule)
					db.session.commit()
			
			print "Request Status: " + str(trains_page.status_code) + "; Request Time: " + str(request_time)

			db.session.add(Requests(url, request_time))
			db.session.add(station)
			db.session.commit()

	print "Completed."

	if i < 9:
		print "Iteration " + str(i) + ", sleeping..."
		time.sleep(30)
