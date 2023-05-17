import flask_wtf
import wtforms
from app.models import User


class UserTableForm(flask_wtf.FlaskForm):
    id = wtforms.HiddenField()
    user = wtforms.SelectField('User', choices=[], validators=[wtforms.validators.InputRequired()])

    def set_choices(self):
        self.user.choices = [(u.id, u.name) for u in User.query.all() if not u.admin]


class TaskEditForm(flask_wtf.FlaskForm):
    details = wtforms.StringField("Name of task", validators=[wtforms.validators.DataRequired()])
    hours = wtforms.DecimalField("Hours spent on task", places=2)
    description = wtforms.TextAreaField("Description of task")
    upload = wtforms.FileField('Add new file')


class ProjectEditForm(flask_wtf.FlaskForm):
    name = wtforms.StringField("Name of project", validators=[wtforms.validators.DataRequired()])
    description = wtforms.TextAreaField("Description of project")
    hour_rate = wtforms.IntegerField("Hour rate")
    upload = wtforms.FileField('Add new file')
