from flask import render_template
from flask.views import MethodView
from flask_smorest import Blueprint, abort

IndexBlueprint = Blueprint('index', 'index', url_prefix='/', template_folder='app/resources/templates')

@IndexBlueprint.route('/')
class Index(MethodView):
    def get(self):
        return render_template('index.html')