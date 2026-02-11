from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, email

class LoginForm(FlaskForm):
  email = StringField(label="Email", validators=[DataRequired(), email()])
  password = PasswordField(label="Password", validators=[DataRequired()])
  submit = SubmitField(label="Log In")