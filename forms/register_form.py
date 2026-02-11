from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import email, DataRequired

class RegisterForm(FlaskForm):
  name = StringField(label="Name", validators=[DataRequired()])
  email = StringField(label="Email", validators=[DataRequired(), email(message="Not a valid email.")])
  password = PasswordField(label="Password", validators=[DataRequired()])
  submit = SubmitField(label="Register")