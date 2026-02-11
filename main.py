from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from helpers.decorators import authorized
from helpers.gravatar_helper import gravatar_url
from utils.extensions import db
from models.blogpost import BlogPost
from models.comments import Comment
from models.user import User
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.blogpost_form import PostForm
from forms.comment_form import CommentForm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash 
from helpers.get_year_helper import get_current_year
from dotenv import load_dotenv
from flask_migrate import Migrate
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
db_url = os.environ.get("DATABASE_URL") or os.environ.get("SQLALCHEMY_DATABASE_URI")

if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url

app.jinja_env.globals["gravatar_url"] = gravatar_url
db.init_app(app)
Bootstrap5(app)
CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
  return db.session.get(User, int(user_id))

@app.route("/")
def home():
  stmt = db.select(BlogPost)
  posts = db.session.scalars(stmt).all()
  return render_template("home.html", posts=posts, user=current_user, logged_in=current_user.is_authenticated, year=get_current_year())

@app.route("/post/<int:post_id>")
def show_post(post_id):
  post = db.get_or_404(BlogPost, post_id)
  return render_template("post.html", post=post, comments=post.comments, user=current_user, logged_in=current_user.is_authenticated, year=get_current_year())

@app.route("/post/new", methods=["GET", "POST"])
@login_required
@authorized
def create_post():
  current_date = datetime.now().strftime("%B %d, %Y")
  form = PostForm()
  if form.validate_on_submit():
    new_post = BlogPost(
      title=form.title.data,
      subtitle=form.subtitle.data,
      body=form.body.data,
      date=current_date,
      img_url=form.img_url.data,
      author_id=current_user.id
    )
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('home'))
  return render_template("create_post.html", form=form, user=current_user, logged_in=current_user.is_authenticated, year=get_current_year())

@app.route("/post/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
@authorized
def edit_post(post_id):
  post = db.get_or_404(BlogPost, post_id)
  form = PostForm(obj=post)
  if form.validate_on_submit():
    post.title = form.title.data
    post.subtitle = form.subtitle.data
    post.body = form.body.data
    post.img_url = form.img_url.data
    
    db.session.commit()
    return redirect(url_for('home'))
  return render_template("create_post.html", form=form, post=post, logged_in=current_user.is_authenticated, edit=True, year=get_current_year())

@app.route("/post/delete/<int:post_id>")
@login_required
@authorized
def delete_post(post_id):
  post = db.get_or_404(BlogPost, post_id)
  
  db.session.delete(post)
  db.session.commit()
  return redirect(url_for("home"))

@app.route("/post/comment/<int:post_id>", methods=["GET", "POST"])
@login_required
def comment(post_id):
  post = db.get_or_404(BlogPost, post_id)
  
  form = CommentForm()
  if form.validate_on_submit():
    new_comment = Comment(
      text=form.text.data,
      author_id=current_user.id,
      post_id=post_id
    )
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))
  return render_template("post.html", post=post, form=form, comments=post.comments, user=current_user, logged_in=current_user.is_authenticated, year=get_current_year())
  

@app.route("/user/register", methods=["GET", "POST"])
def register():
  form = RegisterForm()
  
  
  if form.validate_on_submit():
    hashed_password = generate_password_hash(
      password=form.password.data,
      method="pbkdf2:sha256",
      salt_length=8
    )
    
    new_user = User(
      name=form.name.data,
      email=form.email.data,
      password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user)
    return redirect(url_for('home'))
  return render_template("register.html", form=form, logged_in=current_user.is_authenticated, year=get_current_year())

@app.route("/user/login", methods= ["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    stmt = db.select(User).where(User.email == form.email.data)
    user = db.session.scalar(stmt)
    
    if not user:
      flash("Email not found in database.")
    elif not check_password_hash(user.password, form.password.data):
      flash("Incorrect password")
    else:
      login_user(user)
      return redirect(url_for('home'))
  return render_template("login.html", form=form, logged_in=current_user.is_authenticated, year=get_current_year())

@app.route("/user/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('home'))

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True, port=5050)