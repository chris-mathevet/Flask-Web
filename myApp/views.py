from .app import app, db
from . import models as mod

from hashlib import sha256

from flask import render_template, url_for, redirect,request
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms. validators import DataRequired

from flask_login import login_user , current_user, logout_user, login_required

class AuthorForm(FlaskForm):
    id = HiddenField ("id")
    name = StringField("Nom",validators =[DataRequired()])

class LoginForm ( FlaskForm ):
    username = StringField ("Username")
    password = PasswordField ("Password")
    next = HiddenField()
    def get_authenticated_user (self):
        user = mod.User.query.get(self.username.data)
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
            nextPage = f.next.data or url_for("home")
            return redirect(nextPage)
    return render_template (
        "login.html",
        form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template(
        "home.html",
        title="My Books !",
        books=mod.get_sample())

# View

@app.route("/view/book/<id>")
def detail(id):
    return render_template(
        "detail.html",
        book=mod.get_book_by_id(int(id)))

@app.route("/view/author/<id>")
def one_author(id):
    return render_template(
        "author.html",
        author = mod.get_author_by_id(int(id)),
        books = mod.get_books_by_author(int(id)))

# Edit

@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = mod.get_author_by_id(id)
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
        a = mod.get_author_by_id(int(f.id.data))
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for("one_author", id=a.id))
    a = mod.get_author_by_id(int(f.id.data))
    return render_template("edit-author.html", author=a, form=f)

# Add

@app.route("/add/author/")
@login_required
def add_author():
    f = AuthorForm(id=None, name="")
    return render_template (
        "add-author.html",
        form=f)

@app.route("/add/author/save", methods =("POST",))
@login_required
def save_new_author(new=False):
    print(new)
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        a = mod.Author(name=f.name.data)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for("one_author", id=a.id))
    return render_template("edit-author.html", author=a, form=f)


@app.route("/view/author")
def list_author():
    lim = int(request.args.get('lim', 10))  # Par défaut à 10 si pas de paramètre 'lim'

    return render_template(
        "authors.html",
        title="Authors",
        limiteAutheur=lim,
        authors=mod.get_sample_authors(lim))
# User

@app.route("/user/favorites/")
@login_required
def favorite_books():
    return render_template(
            "favorites.html",
            books=current_user.favorites,
            recommends = mod.recommendations(current_user))

@app.route("/user/favorites/add/<int:book_id>")
@login_required
def add_favorite(book_id):
    mod.add_favorites(current_user,book_id)
    return redirect(url_for("detail",id=book_id))

@app.route("/user/favorites/del/<int:book_id>")
@login_required
def supp_favorite(book_id):
    mod.supp_favorites(current_user,book_id)
    return redirect(url_for("detail",id=book_id))
