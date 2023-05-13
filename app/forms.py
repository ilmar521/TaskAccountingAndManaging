import flask_wtf
import wtforms


class TaskEditForm(flask_wtf.FlaskForm):
    details = wtforms.StringField("Name of task", validators=[wtforms.validators.DataRequired()])
    hours = wtforms.DecimalField("Hours spent on task", places=2)
    description = wtforms.StringField("Description of task")
    upload = wtforms.FileField('Add new file')


class ProjectEditForm(flask_wtf.FlaskForm):
    name = wtforms.StringField("Name of project", validators=[wtforms.validators.DataRequired()])
    description = wtforms.StringField("Description of project")
    hour_rate = wtforms.IntegerField("Hour rate")
    upload = wtforms.FileField('Add new file')
