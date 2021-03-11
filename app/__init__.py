from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

from app.config import DevelopmentConfig,ProductionConfig

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.login_view = 'authentication.do_the_login'
login_manager.session_protection = 'strong'
APP_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app(*,config_object):

	flask_app = Flask(__name__, template_folder='templates',static_folder='static')
	flask_app.config.from_object(config_object)

	db.init_app(flask_app)
	bcrypt.init_app(flask_app)
	login_manager.init_app(flask_app)
	
	from app.catalogue.controller import catalogue
	from app.auth.controller import authentication

	flask_app.register_blueprint(catalogue)
	flask_app.register_blueprint(authentication)

	@flask_app.errorhandler(404)
	def page_not_found(error):
	    return render_template('page_not_found.html'), 404
	return flask_app

	
