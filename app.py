from flask import Flask, render_template, current_app
app = Flask(__name__, static_folder='public/static', template_folder='public/template')

from action.api import api
from controller.databaseAPI import *
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
	def __init__(self, map, *args):
		self.map = map
		self.regex = args[0]

app.url_map.converters['regex'] = RegexConverter

app.register_blueprint(api)
app.register_blueprint(databaseAPI)



from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
	def __init__(self, map, *args):
		self.map = map
		self.regex = args[0]

from model.sqlite import SQliteBridge, getDB, closeDB

def initDB():
	db = getDB()
	with current_app.open_resource('schema.sql') as f:
		db.initDB(f.read().decode('utf8'))


@app.before_first_request
def createDB():
	print("Initial DB.")
	initDB()

@app.teardown_appcontext
def closeConnection(exception):
	closeDB()


@app.route("/")
def mainPage():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()