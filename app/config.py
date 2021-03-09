import os
class Config:
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'this-really-needs-to-be-changed'
	

class ProductionConfig(Config):
	DEBUG = False
	SERVER_PORT = os.environ.get('PORT')
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
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