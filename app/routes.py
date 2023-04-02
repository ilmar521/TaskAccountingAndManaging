import flask
from app import flask_app, db
from app.models import Todo
from flask import flash


@flask_app.route("/", methods=("GET", "POST"))
def index():
    if flask.request.method == "POST":
        task_name = flask.request.form.get("task-name")
        if task_name == '':
            flash('Enter the name of task!')
        else:
            new_task = Todo(details=task_name)
            new_task.save_task_to_db()
    all_tasks = Todo.query.all()
    return flask.render_template('index.html', all_tasks=all_tasks)


@flask_app.route("/complete/<int:todo_id>")
def complete(todo_id):
    task = Todo.query.filter(Todo.id==todo_id).first()
    task.set_task_as_complete()
    return flask.redirect(flask.url_for('index'))


@flask_app.route("/delete/<int:todo_id>")
def delete(todo_id):
    task = Todo.query.filter(Todo.id==todo_id).first()
    db.session.delete(task)
    db.session.commit()
    return flask.redirect(flask.url_for('index'))




