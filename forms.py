from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    department = StringField('Department',validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    submit = SubmitField('Submit')