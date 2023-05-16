from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import User, Task, Project
from sqlalchemy import func, or_
from flask_login import current_user

reports = Blueprint('reports', __name__, template_folder='templates')

from app import db


def main_task_execution_report(selected_user, selected_statuses):

    if not current_user.admin:
        selected_user = current_user

    task_data = db.session.query(
        Project,
        func.sum(Task.hours).label('total_hours'),
        Project.hour_rate,
        func.sum(Task.hours * Project.hour_rate).label('total_amount')
    ).join(Task).filter(
        Task.status.in_(selected_statuses),
        or_(Task.user_id == selected_user, selected_user == 'All')
    ).group_by(Project).all()

    result = {}
    for project, total_hours, hour_rate, total_amount in task_data:
        project_data = {
            'name': project.name,
            'description': project.description,
            'hour_rate': project.hour_rate,
            'total_hours': total_hours,
            'total_amount': total_amount
        }

        project_tasks = project.tasks.all()
        tasks_data = []
        for task in project_tasks:
            task_data = {
                'details': task.details,
                'description': task.description,
                'status': task.status,
                'hours': task.hours,
                'hour_rate': project.hour_rate,
                'total_amount': task.hours * project.hour_rate
            }
            tasks_data.append(task_data)

        project_data['tasks'] = tasks_data
        result[project.id] = project_data

    return render_template('taskExecutionReport_main.html', result=result)


@reports.route('/task_execution_report')
def task_execution_report():
    users = list(User.query.all())
    return render_template('taskExecutionReport.html', users=users)


@reports.route('/task_execution_report/<variant>', methods=['POST'])
def make_task_execution_report(variant):

    data = request.get_json()
    selected_user = data['user_id']
    selected_statuses = data['statuses']
    table_html = ''
    if variant == 'main':
        table_html = main_task_execution_report(selected_user, selected_statuses)
    return table_html
