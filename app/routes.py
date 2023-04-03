import flask
from flask import request
from app import flask_app, db
from app.models import Task, Project
from flask import flash


@flask_app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        project = request.form.getlist('project')
        status = request.form.getlist('status')
        all_projects = Project.query.all()
        all_tasks = list(Task.query.filter(Task.project_id == project[0], Task.status == status[0]))
    else:
        all_projects = Project.query.all()
        all_tasks = list(Task.query.filter(Task.project == all_projects[0], Task.status == 'new'))
    return flask.render_template('index.html', all_tasks=all_tasks, all_projects=all_projects)
#
#
# @flask_app.route("/complete/<int:todo_id>")
# def complete(todo_id):
#     task = Todo.query.filter(Todo.id==todo_id).first()
#     task.set_task_as_complete()
#     return flask.redirect(flask.url_for('index'))
#
#
# @flask_app.route("/delete/<int:todo_id>")
# def delete(todo_id):
#     task = Todo.query.filter(Todo.id==todo_id).first()
#     db.session.delete(task)
#     db.session.commit()
#     return flask.redirect(flask.url_for('index'))




