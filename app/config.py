import os
class Config:
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'this-really-needs-to-be-changed'
	GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
	GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
	GOOGLE_DISCOVERY_URL = (
	    "https://accounts.google.com/.well-known/openid-configuration"
	)
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'thenewonlinebookstore@gmail.com'
	MAIL_PASSWORD = 'AbhishekUser007$'
	

class ProductionConfig(Config):
	DEBUG = False
	SERVER_PORT = os.environ.get('PORT')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',"")
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://abhishek:abhishek@localhost/heroku_app'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SERVER_PORT = 5000

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://abhishek:abhishek@localhost/heroku_app'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SERVER_PORT = 5000