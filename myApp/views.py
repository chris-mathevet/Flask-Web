from .app import app, db
from .models import *
from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms. validators import DataRequired
from wtforms import PasswordField
from .models import User
from hashlib import sha256
from flask_login import login_user , current_user
from flask import request
from flask_login import logout_user, login_required

class AuthorForm(FlaskForm):
    id = HiddenField ("id")
    name = StringField("Nom",validators =[DataRequired()])

class LoginForm ( FlaskForm ):
    username = StringField ("Username")
    password = PasswordField ("Password")
    next = HiddenField()
    def get_authenticated_user (self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256 ()
        m.update(self.password.data.encode ())
        passwd = m. hexdigest ()
        return user if passwd == user.password else None

@app.route("/login/", methods =("GET","POST" ,))
def login():
    f = LoginForm()
    if not f. is_submitted ():
        f.next.data = request.args.get("next")
    elif f. validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template (
        "login.html",
        form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    print(current_user.is_authenticated, "\n\n\n")
    return render_template(
        "home.html",
        title="My Books !",
        books=get_sample())

@app.route("/detail/<id>")
def detail(id):
    return render_template(
        "detail.html",
        book=get_book_by_id(int(id)))

@app.route("/author/<id>")
def one_author(id):
    return render_template(
        "author.html",
        author=get_author_by_id(int(id)),
        books = get_books_by_author(int(id)))

@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = get_author_by_id(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template (
        "edit-author.html",
        author=a, form=f)

@app.route("/save/author/", methods =("POST",))
@login_required
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        a = get_author_by_id(int(f.id.data))
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for("one_author", id=a.id))
    a = get_author_by_id(int(f.id.data))
    return render_template("edit-author.html", author=a, form=f)
# add,author

@app.route("/add/author/")
@login_required
def add_author():
    f = AuthorForm(id=None, name="")
    return render_template (
        "add-author.html",
        form=f)

@app.route("/add/save/author/", methods =("POST",))
@login_required
def save_new_author(new=False):
    print(new)
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        a = Author(name=f.name.data)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for("one_author", id=a.id))
    return render_template("edit-author.html", author=a, form=f)

# @app.route("/save/author/", methods =("POST",))
# def save_author():
#     a = None
#     f = AuthorForm()
#     if f.validate_on_submit():
#         a = get_author_by_id(int(f.id.data))
#         a.name = f.name.data
#         db.session.commit()
#         return redirect(url_for("one_author", id=a.id))
#     a = get_author_by_id(int(f.id.data))
#     return render_template (
#         "edit-author.html",
#         author=a, form=f)
