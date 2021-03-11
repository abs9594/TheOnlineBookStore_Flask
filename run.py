from app import create_app,db
from app.auth.models import User
from app.catalogue.models import Book,Publication
from app.config import DevelopmentConfig,ProductionConfig
from sqlalchemy import exc

flask_app = create_app(config_object=ProductionConfig)

with flask_app.app_context():
	try:
		db.create_all()
		if not(User.query.filter_by(user_name="abhishek007").first()):
			User.create_user(user="abhishek007",email="abs9594@gmail.com",password="AbhishekUser007$")
	except exc.IntegrityError:
		pass
	
	
# if __name__ == '__main__':
# 	flask_app.run()