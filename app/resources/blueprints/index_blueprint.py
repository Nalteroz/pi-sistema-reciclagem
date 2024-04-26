from flask import render_template, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user, JWTManager

IndexBlueprint = Blueprint('index', 'index', url_prefix='/', template_folder='app/resources/templates')

@IndexBlueprint.route('/')
class Index(MethodView):
    @jwt_required()
    def get(self):
        return render_template('index.html')

@IndexBlueprint.route('/login')
class Login(MethodView):
    def get(self):
        return render_template('login.html')
