import flask
from app import flask_app, db
from app.models import Task, Project, AttachmentProjects, AttachmentTasks
from app.forms import TaskEditForm, ProjectEditForm
from flask import flash, jsonify, redirect, url_for, render_template, request, send_file
from flask_login import current_user
from io import BytesIO
import mimetypes


current_project = None
current_status = None


def count_tasks_by_project(project):
    numbers_of_tasks = {'new': 0, 'in_operation': 0, 'complete': 0,'archive': 0}
    all_tasks = list(Task.query.filter(Task.project_id == project, Task.user_id == current_user.id))
    for task in all_tasks:
        numbers_of_tasks[task.status] += 1
    return numbers_of_tasks


@flask_app.route('/upload/<task_id>', methods=['POST'])
def upload_file(task_id):
    file = request.files['file']
    attachment = AttachmentTasks(name=file.filename, content=file.read(), task_id=task_id)
    db.session.add(attachment)
    db.session.commit()
    return jsonify({'name': attachment.name, 'id': attachment.id})


@flask_app.route('/open/<file_id>', methods=['GET'])
def open_file(file_id):
    file = AttachmentTasks.query.get_or_404(file_id)
    mimetype = mimetypes.guess_type(file.name)[0]
    file_data = BytesIO(file.content)
    return send_file(
        file_data,
        mimetype=mimetype,
        as_attachment=False,
        conditional=True
    )


@flask_app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    file = AttachmentTasks.query.get_or_404(file_id)
    mimetype = mimetypes.guess_type(file.name)[0]
    file_data = BytesIO(file.content)
    return send_file(
        file_data,
        mimetype=mimetype,
        as_attachment=True,
        download_name=file.name
    )


@flask_app.route('/delete_file/<file_id>', methods=['POST'])
def delete_file(file_id):
    file = AttachmentTasks.query.filter(AttachmentTasks.id == int(file_id)).first_or_404()
    with flask_app.app_context():
        current_db_sessions = db.session.object_session(file)
        current_db_sessions.delete(file)
        current_db_sessions.commit()
    return jsonify({'success': True})


@flask_app.route("/", methods=("GET", "POST"))
def index():
    global current_project, current_status

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        projects = request.form.getlist('project')
        statuses = request.form.getlist('status')
        current_project = 0 if len(projects) == 0 else int(projects[0])
        current_status = statuses[0]
        task_name = request.form.get("task-name")
        task_adding = request.form.get("button_add_task")
        if task_adding is not None:
            if task_name == '':
                flash('Enter the name of task!')
            elif current_project == 0:
                flash('Select project for adding new task!')
            else:
                new_task = Task(details=task_name, status='new', hours=0, project_id=current_project, user_id=current_user.id)
                new_task.save_task_to_db()
        all_projects = Project.query.all()
        all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status, Task.user_id == current_user.id))
    else:
        all_projects = Project.query.all()
        if current_project is None:
            current_project = 0 if len(all_projects) == 0 else all_projects[0].id
        if current_status is None:
            current_status = 'in_operation'
        all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status, Task.user_id == current_user.id))
    return render_template('index.html', all_tasks=all_tasks, all_projects=all_projects, current_project=current_project, current_status=current_status, numbers_of_tasks=count_tasks_by_project(current_project))


@flask_app.route("/change_status/<task_id>/<status>", methods=("GET", "POST"))
def change_status(task_id, status):
    task_id = task_id.replace('task-', '')
    status = status.replace('label_', '')
    task = Task.query.filter(Task.id == int(task_id)).first()
    task.change_value('status', status)
    return ""


@flask_app.route("/add_project", methods=("GET", "POST"))
def add_project():
    if request.method == "POST":
        name_new_project = request.form.get("name_new_project")
        hour_rate = request.form.get("hour_rate")
        new_project = Project(name=name_new_project, hour_rate=hour_rate)
        new_project.save_to_db()
        return redirect(url_for('index'))


@flask_app.route('/task/<id>/edit', methods=['GET', 'POST'])
def task_edit(id):
    task = Task.query.filter_by(id=id).first_or_404()
    files = list(AttachmentTasks.query.filter(AttachmentTasks.task_id == id))
    form = TaskEditForm(details=task.details, hours=task.hours, description=task.description)
    if request.method == 'GET':
        form.details.data = task.details
        form.hours.data = task.hours
    else:
        task.change_value('details', form.details.data)
        task.change_value('hours', form.hours.data)
        # filename = images.save(form.upload.data)
        return jsonify(status='ok')
    return render_template('_task_edit.html', title="Edit task", form=form, files=files, task=task)


@flask_app.route("/delete_task/<task_id>", methods=("GET", "POST"))
def delete_task(task_id):
    task = Task.query.filter(Task.id == int(task_id)).first_or_404()
    with flask_app.app_context():
        current_db_sessions = db.session.object_session(task)
        current_db_sessions.delete(task)
        current_db_sessions.commit()
    return ""


@flask_app.route('/project/<id>/edit', methods=['GET', 'POST'])
def project_edit(id):
    project = Project.query.filter_by(id=id).first_or_404()
    form = ProjectEditForm(name=project.name, hour_rate=project.hour_rate)
    if request.method == 'GET':
        form.name.data = project.name
        form.hour_rate.data = project.hour_rate
    else:
        project.change_value('name', form.name.data)
        project.change_value('hour_rate', form.hour_rate.data)
        return jsonify(status='ok')
    return render_template('_project_edit.html', title="Edit project", form=form)


@flask_app.route("/delete_project/<project_id>", methods=("GET", "POST"))
def delete_project(project_id):
    project = Project.query.filter(Project.id == int(project_id)).first_or_404()
    with flask_app.app_context():
        all_tasks = list(Task.query.filter(Task.project_id == project.id))
        current_db_sessions = db.session.object_session(project)
        current_db_sessions.delete(project)
        current_db_sessions.commit()
        for task in all_tasks:
            current_db_sessions = db.session.object_session(task)
            current_db_sessions.delete(task)
            current_db_sessions.commit()
    return ""


@flask_app.route('/health')
def health():
    return "ok"