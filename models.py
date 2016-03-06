from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

import datetime
import keys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = keys.get_mysql_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('njtransit', MigrateCommand)

class Stations(db.Model):

	__tablename__ = "stations"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	abbr = db.Column(db.String(255))
	schedules = relationship("Schedule", backref="stations", single_parent=True, cascade="all, delete-orphan", primaryjoin=("Stations.id==Schedule.station_id"))

	def __init__(self, name, abbr):
		self.name = name
		self.abbr = abbr

class Schedule(db.Model):

	__tablename__ = "schedule"

	id = db.Column(db.Integer, primary_key=True)
	departure = db.Column(db.String(255))
	to = db.Column(db.String(255))
	track = db.Column(db.String(255))
	line = db.Column(db.String(255))
	train = db.Column(db.String(255))
	status = db.Column(db.String(255))
	station_id = db.Column(db.Integer, ForeignKey("stations.id"))
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	def __init__(self, departure, to, track, line, train, status):
		self.departure = departure
		self.to = to
		self.track = track
		self.line = line
		self.train = train
		self.status = status

class Requests(db.Model):

	__tablename__ = "requests"

	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(255))
	time = db.Column(db.Float)
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	version = db.Column(db.Integer)

	def __init__(self, url, time, version):
		self.url = url
		self.time = time
		self.version = version

if __name__ == "__main__":
	manager.run()
