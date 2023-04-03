from app import flask_app, db
from app.models import Task, Project


def generate():

    p1 = Project(name='Test prj 1')
    p2 = Project(name='Test prj 2')

    t1 = Task(details='Task test prj 1 new', project=p1, status='new')
    t2 = Task(details='Task test prj 1 complete', project=p1, status='complete')
    t3 = Task(details='Task test prj 2 new', project=p2, status='new')
    t4 = Task(details='Task test prj 2 new 2', project=p2, status='new')
    t5 = Task(details='Task test prj 2 in_operation', project=p2, status='in_operation')

    with flask_app.app_context():
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(t1)
        db.session.add(t2)
        db.session.add(t3)
        db.session.add(t4)
        db.session.add(t5)
        db.session.commit()


generate()

