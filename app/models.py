from app import flask_app, db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    details = db.Column(db.Text)
    status = db.Column(db.String(20))
    hours = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def save_task_to_db(self):
        with flask_app.app_context():
            db.session.add(self)
            db.session.commit()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    tasks = db.relationship('Task', backref='project', lazy='dynamic')

