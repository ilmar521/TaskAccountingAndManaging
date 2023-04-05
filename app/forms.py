import flask_wtf
import wtforms


class TaskEditForm(flask_wtf.FlaskForm):
    details = wtforms.StringField("Details of task", validators=[wtforms.validators.DataRequired()])
    hours = wtforms.DecimalField("Hours spent on task", places=2)


class ProjectEditForm(flask_wtf.FlaskForm):
    name = wtforms.StringField("Name of project", validators=[wtforms.validators.DataRequired()])
    hour_rate = wtforms.IntegerField("Hour rate")
