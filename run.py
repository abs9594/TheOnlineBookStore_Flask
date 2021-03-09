from app import create_app,db
from app.auth.models import User
from app.catalogue.models import Book,Publication
from app.config import DevelopmentConfig,ProductionConfig

application = create_app(config_object=ProductionConfig)
with application.app_context():
	db.create_all()
	if not(User.query.filter_by(user_name="abhishek").first()):
		User.create_user(user="abhishek",email="abhishek",password="AbhishekUser007$")

# if __name__ == '__main__':
application.run()