from app import flask_app, db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    details = db.Column(db.Text)
    completed = db.Column(db.Boolean)

    def save_task_to_db(self):
        with flask_app.app_context():
            db.session.add(self)
            db.session.commit()



