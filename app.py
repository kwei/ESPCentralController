from flask import Flask, render_template, current_app
app = Flask(__name__, static_folder='public/static', template_folder='public/template')

from action.api import api
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app.url_map.converters['regex'] = RegexConverter

app.register_blueprint(api)



from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]



if __name__ == "__main__":
    app.run()