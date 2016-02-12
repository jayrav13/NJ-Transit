from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

import keys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = keys.get_mysql_uri()

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('njtransit', MigrateCommand)

class Stations(db.Model):

	__tablename__ = "stations"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	abbr = db.Column(db.String(255))
	version = db.Column(db.Integer)

	def __init__(self, name, abbr, version):
		self.name = name
		self.abbr = abbr
		self.version = version

class Schedule(db.Model):

	__tablename__ = "schedule"

	id = db.Column(db.Integer, primary_key=True)
	departure = db.Column(db.String(255))
	to = db.Column(db.String(255))
	track = db.Column(db.String(255))
	line = db.Column(db.String(255))
	train = db.Column(db.String(255))
	status = db.Column(db.String(255))

	def __init__(self, departure, to, track, line, train, status):
		self.departure = departure
		self.to = to
		self.track = track
		self.line = line
		self.train = train
		self.status = status

if __name__ == "__main__":
	manager.run()
