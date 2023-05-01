import flask
from config import Config
import flask_sqlalchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import flask_migrate
import os

flask_app = flask.Flask(__name__)
flask_app.config.from_object(Config)
basedir = os.path.abspath(os.path.dirname(__file__))

# flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'task_system.db')

db = flask_sqlalchemy.SQLAlchemy(flask_app)
migrate = flask_migrate.Migrate(flask_app, db)
bootstrap = Bootstrap(flask_app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(flask_app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# blueprint for auth routes in our app
from app.auth.auth import auth as auth_blueprint
flask_app.register_blueprint(auth_blueprint)

from app import models, routes
