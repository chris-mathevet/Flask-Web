from .app import app, db
from .models import *
from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms. validators import DataRequired

class AuthorForm(FlaskForm):
    id = HiddenField ("id")
    name = StringField("Nom",validators =[DataRequired()])

@app.route("/")
def home():
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
def edit_author(id):
    a = get_author_by_id(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template (
        "edit-author.html",
        author=a, form=f)

@app.route("/save/author/", methods =("POST",))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit ():
        a = get_author_by_id(int(f.id.data))
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for("one_author", id=a.id))
    a = get_author_by_id(int(f.id.data))
    return render_template (
        "edit-author.html",
        author=a, form=f)