import flask
from flask import request
from app import flask_app, db
from app.models import Task, Project
from app.forms import TaskEditForm
from flask import flash

current_project = None
current_status = None


@flask_app.route("/", methods=("GET", "POST"))
def index():
    global current_project, current_status
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
        if current_project is None:
            current_project = all_projects[0].id
        if current_status is None:
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


@flask_app.route("/add_project", methods=("GET", "POST"))
def add_project():
    if request.method == "POST":
        name_new_project = request.form.get("name_new_project")
        hour_rate = request.form.get("hour_rate")
        new_project = Project(name=name_new_project, hour_rate=hour_rate)
        new_project.save_to_db()
        return flask.redirect(flask.url_for('index'))


@flask_app.route('/task/<id>/edit', methods=['GET', 'POST'])
def task_edit(id):
    task = Task.query.filter_by(id=id).first_or_404()
    form = TaskEditForm(details=task.details, hours=task.hours)
    if request.method == 'GET':
        form.details.data = task.details
        form.hours.data = task.hours
    else:
        task.change_value('details', form.details.data)
        task.change_value('hours', form.hours.data)
        # return jsonify(status='ok')
    return flask.render_template('_task_edit.html', title="Edit task", form=form)


@flask_app.route("/delete_task/<task_id>", methods=("GET", "POST"))
def delete_task(task_id):
    task = Task.query.filter(Task.id == int(task_id)).first_or_404()
    with flask_app.app_context():
        current_db_sessions = db.session.object_session(task)
        current_db_sessions.delete(task)
        current_db_sessions.commit()
    return ('')