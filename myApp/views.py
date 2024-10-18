from .app import app, db
from . import models as mod

from hashlib import sha256

from flask import render_template, url_for, redirect,request
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms. validators import DataRequired, Length

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


class SignupForm ( FlaskForm ):
    username = StringField ("Username")
    password = PasswordField ("Password")
    next = HiddenField()

class SearchForm( FlaskForm ):
    search = StringField("Search")
    def getSearch(self):
        return self.search.data
    
class CommentForm( FlaskForm ):
    comment = StringField("Comment",validators =[DataRequired(), Length(max=149)])
    
@app.route("/search/", methods =("GET","POST" ,))
def search():
    f = SearchForm()
    srch = request.args.get("searchBar","")
    if srch == "":
        return redirect("https://www.yout-ube.com/watch?v=uHgt8giw1LY&autoplay=1")
    elif srch.lower() == "quoi":
        return redirect("https://www.yout-ube.com/watch?v=5i5T_vE9RfU")
    elif srch.lower() == "triste":
        return redirect("https://www.yout-ube.com/watch?v=8yPfLXZD4pk")
    else:
        return render_template(
            "search.html",
            search = srch,
            books=mod.get_book_by_title(srch),
            authors = mod.get_athor_by_name(srch))


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


@app.route("/signup/", methods=["GET", "POST"])
def register():
    f = SignupForm()
    if request.method == "POST":
        # Validate form data
        username = request.form.get("username")
        password = request.form.get("password")

        if not (username and password):
            return render_template("singup.html", message="All fields are required.")
        if f.validate_on_submit():
            user = mod.User.query.get(username)
            if user is None:
                from .models import User
                from hashlib import sha256
                m = sha256()
                m.update(password.encode())
                new_user = User(username=username , password=m.hexdigest())
                db.session.add(new_user)
                db.session.commit()

        return redirect("/login")

    return render_template("singup.html", form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    lim = int(request.args.get('lim', 10)) 

    return render_template(
        "home.html",
        title="My Books !",
        limiteAutheur=lim,
        books=mod.get_sample(lim))

# View

@app.route("/view/book/<id>", methods =["GET","POST"])
def detail(id):
    f = CommentForm()
    cpt_note,sum_note,moyenne_du_livre = 0,0,0
    
    editT = request.args.get('edit', "False")
    editT = (editT == "True") 
    suppr = request.args.get('suppr', "False")
    
    book = mod.get_book_by_id(int(id))
    print(mod.get_all_comment(book.id))
    for comment in mod.get_all_comment(book.id):
        if comment.note is not None:
            sum_note += comment.note
            cpt_note +=1
    if cpt_note > 0: 
        moyenne_du_livre = sum_note//cpt_note

    if editT:
        f.comment.data = book.get_comment(current_user).comment
    
    if suppr == "True":
        mod.del_comment(current_user,book) 

    if request.method == "POST":
        if f.validate_on_submit():
            comment = f.comment.data
            mod.add_edit_comment(current_user,book,comment)
    return render_template(
        "detail.html",
        book=book,
        edit=editT,
        moyenne= moyenne_du_livre,
        form = f)

@app.route("/view/author/<id>")
def one_author(id):
    return render_template(
        "author.html",
        author = mod.get_author_by_id(int(id)),
        books = mod.get_books_by_author(int(id)))

@app.route("/view/author")
def list_author():
    lim = int(request.args.get('lim', 10)) 

    return render_template(
        "authors.html",
        title="Authors",
        limiteAutheur=lim,
        authors=mod.get_sample_authors(lim))
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
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        a = mod.Author(name=f.name.data)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for("one_author", id=a.id))
    return render_template("edit-author.html", author=a, form=f)

@app.route("/add/comment/<int:book_id>/<form>", methods =("POST",))
@login_required
def add_comment(book_id, form):
    # comment = request.args.get("comment",None)
    print(form)
    # if comment:
        # if form.validate_on_submit():
        #     book = mod.get_book_by_id(book_id)
        #     mod.add_edit_comment(current_user,book,comment)
        #     return redirect(url_for("detail",id=book_id))
    return redirect(url_for("detail",id=book_id))

@app.route("/add/note/<id>/<lanote>", methods =("POST","GET"))
@login_required
def noter(id, lanote):
    print("note:" + lanote)
    book = mod.get_book_by_id(int(id))
    mod.add_edit_note(current_user,book,int(lanote))
    return redirect(url_for("detail",id=id))

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

# TKT

@app.route("/mais/ca/nexiste/pas/")
def disable_page():
    return render_template(
        "disabled.html")

@app.errorhandler(404)
@app.route("/mais/ca/nexiste/pas/")
def page_not_found(e):
    return redirect(url_for('disable_page'))

