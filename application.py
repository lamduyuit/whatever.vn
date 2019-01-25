from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mail import Mail

from flask_login import LoginManager

mail = Mail()
login_manager = LoginManager()
login_manager.login_view  = "user_app.login"
#login_manager.login_message = "Ban can dang nhap"

db = MongoEngine()

def create_app(**config_overrides):

    app = Flask(__name__,instance_path="/home/lamduyuit/apps/home/data/download_financial/")
    app.config.from_pyfile('settings.py')
    
    app.config.update(config_overrides)
    
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    
    from home.views import home_app
    from user.views import user_app

    app.register_blueprint(user_app)
    app.register_blueprint(home_app)
    
    return app