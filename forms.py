from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class RegistrationForm(FlaskForm):
    username = StringField(label='Name', validators=[DataRequired("Username cannot be null"), Length(min=2, max=20)])
    age = FloatField(label='Age', validators=[DataRequired("Age cannot be null")])
    email = StringField(label='Email', validators=[DataRequired("Email cannot be null"), Email("Invalid email address")])
    weight = FloatField(label='Weight', validators=[DataRequired("Weight cannot be null")])
    height = FloatField(label='Height', validators=[DataRequired("Height cannot be null")])
    bodyfat = FloatField(label='Body Fat Percentage', validators=[DataRequired("Body Fat Percentage cannot be null")])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Login')
