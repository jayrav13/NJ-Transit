from models import db, Stations
from lxml import html
import requests
import sys

# Request all stations, parse into html tree
stations_page = requests.get('http://m.njtransit.com/mo/mo_servlet.srv?hdnPageAction=DvTo')
stations_tree = html.document_fromstring(stations_page.text)

# Begin session, try to scrape and commit
version = db.session.query(db.func.max(Stations.version)).scalar()
if version == None:
	version = 0

version = version + 1

for val in stations_tree.xpath('//option'):
	if(len(val.attrib['value'])):
		station = Stations(val.text, val.attrib['value'], version)

		trains_page = requests.get('http://dv.njtransit.com/mobile/tid-mobile.aspx?sid=' + val.attrib['value'])
		trains_tree = html.document_fromstring(trains_page.text)

		for elem in trains_tree.xpath('//table'):
		#	for tr in elem.xpath('tr'):
		#		for td in tr.xpath('td'):
		#			print td.text
			for tr in elem.getchildren():
				if len(tr) > 3:
					for td in tr.getchildren():
						print td.text

		print trains_page.status_code

		db.session.add(station)
		db.session.commit()

