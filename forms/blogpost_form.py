from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):
  title = StringField(label="Title", validators=[DataRequired()])
  subtitle = StringField(label="Subtitle", validators=[DataRequired()])
  body = CKEditorField(label="Body", validators=[DataRequired()])
  img_url = StringField(label="Image Url", validators=[DataRequired(), URL()])
  submit = SubmitField(label="Submit Post")