from .app import app
from flask import render_template
from .models import *
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

@app.route("/edit/author/<int:id>")
def edit_author (id):
    a = get_author_by_id(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template (
        "edit-author.html",
        author=a, form=f)