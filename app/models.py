from app import flask_app, db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    details = db.Column(db.Text)
    status = db.Column(db.String(20))
    hours = db.Column(db.Float, default=0)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def save_task_to_db(self):
        with flask_app.app_context():
            db.session.add(self)
            db.session.commit()

    def change_value(self, type_value, new_value):
        with flask_app.app_context():
            self[type_value] = new_value
            current_db_sessions = db.session.object_session(self)
            current_db_sessions.add(self)
            current_db_sessions.commit()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    hour_rate = db.Column(db.Integer)
    tasks = db.relationship('Task', backref='project', lazy='dynamic')

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def save_to_db(self):
        with flask_app.app_context():
            db.session.add(self)
            db.session.commit()

    def change_value(self, type_value, new_value):
        with flask_app.app_context():
            self[type_value] = new_value
            current_db_sessions = db.session.object_session(self)
            current_db_sessions.add(self)
            current_db_sessions.commit()

