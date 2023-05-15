from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import User

reports = Blueprint('reports', __name__, template_folder='templates')

from app import db


@reports.route('/task_execution_report')
def task_execution_report():
    users = list(User.query.all())
    return render_template('taskExecutionReport.html', users=users)
