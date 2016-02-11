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

	def __init__(self, name, abbr):
		self.name = name
		self.abbr = abbr

if __name__ == "__main__":
	manager.run()
