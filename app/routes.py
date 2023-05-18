import flask
from app import flask_app, db
from app.models import Task, Project, AttachmentProjects, AttachmentTasks, NotesTasks, NotesProjects, User
from app.forms import TaskEditForm, ProjectEditForm, UserTableForm
from flask import flash, jsonify, redirect, url_for, render_template, request, send_file
from flask_login import current_user
from io import BytesIO
import mimetypes
from datetime import datetime


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


@flask_app.route('/upload_prj/<prj_id>', methods=['POST'])
def upload_prj_file(prj_id):
    file = request.files['file']
    attachment = AttachmentProjects(name=file.filename, content=file.read(), project_id=prj_id)
    db.session.add(attachment)
    db.session.commit()
    return jsonify({'name': attachment.name, 'id': attachment.id})


@flask_app.route('/open_prj/<prj_id>', methods=['GET'])
def open_prj_file(prj_id):
    file = AttachmentProjects.query.get_or_404(prj_id)
    mimetype = mimetypes.guess_type(file.name)[0]
    file_data = BytesIO(file.content)
    return send_file(
        file_data,
        mimetype=mimetype,
        as_attachment=False,
        conditional=True
    )


@flask_app.route('/download_prj/<prj_id>', methods=['GET'])
def download_prj_file(prj_id):
    file = AttachmentProjects.query.get_or_404(prj_id)
    mimetype = mimetypes.guess_type(file.name)[0]
    file_data = BytesIO(file.content)
    return send_file(
        file_data,
        mimetype=mimetype,
        as_attachment=True,
        download_name=file.name
    )


@flask_app.route('/delete_prj_file/<prj_id>', methods=['POST'])
def delete_prj_file(prj_id):
    file = AttachmentProjects.query.filter(AttachmentProjects.id == int(prj_id)).first_or_404()
    with flask_app.app_context():
        current_db_sessions = db.session.object_session(file)
        current_db_sessions.delete(file)
        current_db_sessions.commit()
    return jsonify({'success': True})


@flask_app.route('/add_note/<task_id>', methods=['POST'])
def add_note(task_id):
    detail = request.form.get("detail")
    note = NotesTasks(detail=detail, task_id=task_id, date=datetime.now())
    db.session.add(note)
    db.session.commit()
    return jsonify({'detail': note.detail, 'id': note.id, 'date': note.date.strftime('%Y-%m-%d')})


@flask_app.route('/add_note_prj/<prj_id>', methods=['POST'])
def add_note_prj(prj_id):
    detail = request.form.get("detail")
    note = NotesProjects(detail=detail, project_id=prj_id, date=datetime.now())
    db.session.add(note)
    db.session.commit()
    return jsonify({'detail': note.detail, 'id': note.id, 'date': note.date.strftime('%Y-%m-%d')})


def get_allowed_projects():
    if current_user.admin:
        return Project.query.order_by(Project.id).all()
    return Project.query.join(Project.users).filter(User.id == current_user.id).order_by(Project.id).all()


@flask_app.route("/change_task_area", methods=("GET", "POST"))
def change_task_area():
    global current_project, current_status

    projects = request.form.getlist('project')
    statuses = request.form.getlist('status')
    current_project = 0 if len(projects) == 0 else int(projects[0])
    current_status = statuses[0]
    all_projects = get_allowed_projects()
    all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status,
                                       Task.user_id == current_user.id))
    return render_template('task_area.html', all_tasks=all_tasks, all_projects=all_projects, current_project=current_project, current_status=current_status, numbers_of_tasks=count_tasks_by_project(current_project))


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
        all_projects = get_allowed_projects()
        all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status, Task.user_id == current_user.id).order_by(Task.id))
    else:
        all_projects = get_allowed_projects()
        if current_project is None:
            current_project = 0 if len(all_projects) == 0 else all_projects[0].id
        if current_status is None:
            current_status = 'in_operation'
        all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status, Task.user_id == current_user.id).order_by(Task.id))
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


@flask_app.route("/add_task", methods=['POST'])
def add_task():
    global current_project, current_status

    projects = request.form.getlist('project')
    current_project = 0 if len(projects) == 0 else int(projects[0])
    current_status = "new"
    task_name = request.form.get("task-name")
    if task_name == '':
        flash('Enter the name of task!')
    elif current_project == 0:
        flash('Select project for adding new task!')
    else:
        new_task = Task(details=task_name, status='new', hours=0, project_id=current_project,
                        user_id=current_user.id)
        new_task.save_task_to_db()

    all_projects = get_allowed_projects()
    all_tasks = list(Task.query.filter(Task.project_id == current_project, Task.status == current_status,
                                       Task.user_id == current_user.id).order_by(Task.id))
    return render_template('task_area.html', all_tasks=all_tasks, all_projects=all_projects,
                           current_project=current_project, current_status=current_status,
                           numbers_of_tasks=count_tasks_by_project(current_project))


@flask_app.route('/task/<id>/edit', methods=['GET', 'POST'])
def task_edit(id):
    task = Task.query.filter_by(id=id).first_or_404()
    files = list(AttachmentTasks.query.filter(AttachmentTasks.task_id == id))
    notes = list(NotesTasks.query.filter(NotesTasks.task_id == id).order_by(NotesTasks.date.desc()).all())
    form = TaskEditForm(details=task.details, hours=task.hours, description=task.description)
    if request.method == 'GET':
        form.details.data = task.details
        form.hours.data = task.hours
        form.description.data = task.description
    else:
        if task.details != form.details.data or task.hours != form.hours.data or task.description != form.description.data:
            with flask_app.app_context():
                task.details = form.details.data
                task.hours = form.hours.data
                task.description = form.description.data
                current_db_sessions = db.session.object_session(task)
                current_db_sessions.add(task)
                current_db_sessions.commit()
            return jsonify(status='updated')
        return jsonify(status='close')
    return render_template('_task_edit.html', title="Edit task", form=form, files=files, notes=notes, task=task)


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
    users = project.users
    files = list(AttachmentProjects.query.filter_by(project_id=id))
    notes = list(NotesProjects.query.filter_by(project_id=id).order_by(NotesProjects.date.desc()).all())
    form = ProjectEditForm(name=project.name, hour_rate=project.hour_rate, description=project.description)
    form_add = UserTableForm()
    form_add.set_choices()
    if request.method == 'GET':
        form.name.data = project.name
        form.hour_rate.data = project.hour_rate
        form.description.data = project.description
    else:
        status = 'close'
        if current_user.admin:
            user_ids = request.form.getlist('user_ids[]')
            users = User.query.filter(User.id.in_(user_ids)).all()
            if set(user_ids) != set(user.id for user in project.users):
                project.users = users
                db.session.commit()
        if project.name != form.name.data or project.hour_rate != form.hour_rate.data or project.description != form.description.data:
            if project.name != form.name.data:
                status = 'updated'
            with flask_app.app_context():
                project.name = form.name.data
                project.hour_rate = form.hour_rate.data
                project.description = form.description.data
                db.session.merge(project)
                db.session.commit()
        return jsonify(status=status)
    return render_template('_project_edit.html', title="Edit project", form=form, files=files, notes=notes, project=project, form_add=form_add, users=users)


@flask_app.route("/delete_project/<project_id>", methods=("GET", "POST"))
def delete_project(project_id):
    project = Project.query.filter(Project.id == int(project_id)).first_or_404()
    with flask_app.app_context():
        current_db_sessions = db.session.object_session(project)
        current_db_sessions.delete(project)
        current_db_sessions.commit()
    return ""


@flask_app.route('/health')
def health():
    return "ok"
