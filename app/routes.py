import flask
from flask import request
from app import flask_app, db
from app.models import Task, Project
from flask import flash


@flask_app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        projects = request.form.getlist('project')
        statuses = request.form.getlist('status')
        current_project = int(projects[0])
        current_status = statuses[0]
        all_projects = Project.query.all()
        all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status))
        return flask.redirect(flask_app.url_for('index', all_tasks=all_tasks, all_projects=all_projects, current_project=current_project, current_status=current_status))
    else:
        all_projects = Project.query.all()
        current_project = all_projects[0].id
        current_status = 'new'
        all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status))
    return flask.render_template('index.html', all_tasks=all_tasks, all_projects=all_projects, current_project=current_project, current_status=current_status)



