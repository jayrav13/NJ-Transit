from flask import Flask, make_response, jsonify, request, abort, render_template
from flask.ext.assets import Environment, Bundle
import requests

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def home():
	return make_response(jsonify({"Success" : "Hello, world!"}), 200)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
