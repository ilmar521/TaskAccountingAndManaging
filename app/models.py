from app import flask_app, db
from flask_login import UserMixin


class AttachmentProjects(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(250))
    content = db.Column(db.LargeBinary)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))


class AttachmentTasks(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(250))
    content = db.Column(db.LargeBinary)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))


class NotesProjects(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    detail = db.Column(db.Text)
    date = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))


class NotesTasks(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    detail = db.Column(db.Text)
    date = db.Column(db.Date)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    admin = db.Column(db.Boolean)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    details = db.Column(db.Text)
    description = db.Column(db.Text)
    status = db.Column(db.String(20))
    hours = db.Column(db.Float, default=0)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    attachments = db.relationship('AttachmentTasks', cascade="all, delete", backref='task', lazy='dynamic')
    notes = db.relationship('NotesTasks', cascade="all, delete", backref='task', lazy='dynamic')

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
    description = db.Column(db.Text)
    hour_rate = db.Column(db.Integer)
    tasks = db.relationship('Task', backref='project', cascade="all, delete", lazy='dynamic')
    attachments = db.relationship('AttachmentProjects', cascade="all, delete", backref='project', lazy='dynamic')
    notes = db.relationship('NotesProjects', cascade="all, delete", backref='project', lazy='dynamic')

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

