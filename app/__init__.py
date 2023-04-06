import flask
from config import Config
import flask_sqlalchemy
from flask_bootstrap import Bootstrap
import flask_migrate
import os

flask_app = flask.Flask(__name__)
flask_app.config.from_object(Config)
basedir = os.path.abspath(os.path.dirname(__file__))

flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'task_system.db')

db = flask_sqlalchemy.SQLAlchemy(flask_app)
migrate = flask_migrate.Migrate(flask_app, db)
bootstrap = Bootstrap(flask_app)

from app import models, routes
