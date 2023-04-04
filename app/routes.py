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
        task_name = request.form.get("task-name")
        task_adding = request.form.get("button_add_task")
        if task_adding is not None:
            if task_name == '':
                flash('Enter the name of task!')
            else:
                new_task = Task(details=task_name, status='new', project_id=current_project)
                new_task.save_task_to_db()
        all_projects = Project.query.all()
        all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status))
    else:
        all_projects = Project.query.all()
        current_project = all_projects[0].id
        current_status = 'new'
        all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status))
    return flask.render_template('index.html', all_tasks=all_tasks, all_projects=all_projects, current_project=current_project, current_status=current_status)


@flask_app.route("/change_status/<task_id>/<status>", methods=("GET", "POST"))
def change_status(task_id, status):
    task_id = task_id.replace('task-', '')
    status = status.replace('label_', '')
    task = Task.query.filter(Task.id == int(task_id)).first()
    task.change_value('status', status)
    return ('')

