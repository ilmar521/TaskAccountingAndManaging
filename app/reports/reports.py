from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import User, Task, Project
from sqlalchemy import func, text
from flask_login import current_user

reports = Blueprint('reports', __name__, template_folder='templates')

from app import db


def main_task_execution_report(selected_user, selected_statuses):
    if not current_user.admin:
        selected_user = current_user.id

    sql_query = text('''
        SELECT
            p.id AS project_id,
            p.name AS project_name,
            p.hour_rate AS project_hour_rate,
            t.id AS task_id,
            t.details AS task_details,
            t.hours AS task_hours,
            t.hours * p.hour_rate AS amount
        FROM
            project p
        JOIN
            task t ON p.id = t.project_id
        WHERE
            t.status IN :selected_statuses
            AND (t.user_id = :selected_user OR :ALL_users)
        GROUP BY
            p.id, p.name, p.hour_rate, t.details, t.id
    ''')

    task_data = db.session.execute(sql_query, {'selected_statuses': tuple(selected_statuses), 'selected_user': 0 if selected_user == 'All' else selected_user, 'ALL_users': True if selected_user == 'All' else False})

    result = {}
    total_hours = 0
    total_amount = 0
    for row in task_data:
        project_id = row[0]
        if project_id not in result:
            project_data = {
                'name': row[1],
                'hour_rate': row[2],
                'total_hours': 0,
                'total_amount': 0,
                'tasks': []
            }
            result[project_id] = project_data

        hours = row[5]
        amount = row[6]
        project_data = result[project_id]
        project_data['total_hours'] += hours
        project_data['total_amount'] += amount
        total_hours += hours
        total_amount += amount

        task_data = {
            'details': row[4],
            'hours': row[5],
            'total_amount': row[6]
        }
        project_data['tasks'].append(task_data)

    return render_template('taskExecutionReport_main.html', result=result, total_hours=total_hours, total_amount=total_amount)


def users_task_execution_report(selected_user, selected_statuses):

    sql_query = text('''
        SELECT
            p.id AS project_id,
            p.name AS project_name,
            p.hour_rate AS project_hour_rate,
            t.id AS task_id,
            t.details AS task_details,
            t.hours AS task_hours,
            t.hours * p.hour_rate AS amount,
            u.name AS user_name
        FROM
            project p
        JOIN
            task t ON p.id = t.project_id
        JOIN
            "user" u ON t.user_id = u.id
        WHERE
            t.status IN :selected_statuses
            AND (t.user_id = :selected_user OR :ALL_users)
        GROUP BY
            p.id, p.name, p.hour_rate, t.details, t.id, u.name
    ''')

    task_data = db.session.execute(sql_query, {'selected_statuses': tuple(selected_statuses), 'selected_user': 0 if selected_user == 'All' else selected_user, 'ALL_users': True if selected_user == 'All' else False})

    result = {}
    total_hours = 0
    total_amount = 0
    for row in task_data:
        user_name = row[7]
        project_id = row[0]

        if user_name not in result:
            user_data = {
                'name': user_name,
                'total_hours': 0,
                'total_amount': 0,
                'projects': {}
            }
            result[user_name] = user_data

        user_data = result[user_name]

        if project_id not in user_data['projects']:
            project_data = {
                'name': row[1],
                'hour_rate': row[2],
                'total_hours': 0,
                'total_amount': 0,
                'tasks': []
            }
            user_data['projects'][project_id] = project_data

        hours = row[5]
        amount = row[6]
        project_data = user_data['projects'][project_id]
        project_data['total_hours'] += hours
        project_data['total_amount'] += amount
        user_data['total_hours'] += hours
        user_data['total_amount'] += amount
        total_hours += hours
        total_amount += amount

        task_data = {
            'details': row[4],
            'hours': row[5],
            'total_amount': row[6]
        }
        project_data['tasks'].append(task_data)

    return render_template('taskExecutionReport_by_users.html', result=result, total_hours=total_hours, total_amount=total_amount)


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
    elif variant == 'users':
        table_html = users_task_execution_report(selected_user, selected_statuses)
    return table_html
