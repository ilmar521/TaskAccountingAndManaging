import flask_wtf
import wtforms


class TaskEditForm(flask_wtf.FlaskForm):
    details = wtforms.StringField("Details of task", validators=[wtforms.validators.DataRequired()])
    hours = wtforms.StringField("Hours spent on task")
