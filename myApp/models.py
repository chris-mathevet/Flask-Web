from .app import db
from flask_login import UserMixin
from .app import login_manager
from sqlalchemy.orm import Mapped
import random

fav_books = db.Table("fav_books",
        db.Column("username",db.String(50),db.ForeignKey("user.username"), primary_key =True),
        db.Column("id_book",db.Integer, db.ForeignKey("book.id"), primary_key =True),
    )

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def get_nb_books_by_author(self):
        print(self.id)
        return len(get_books_by_author(self.id))
    
    def __repr__(self ):
        return self.name

class Book(db.Model):
    id = db.Column(db.Integer , primary_key =True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer , db.ForeignKey("author.id"))
    author = db.relationship("Author",backref=db.backref("books", lazy="dynamic"))
    favorites_book = db.relationship("User",secondary=fav_books,back_populates="favorites")

    def __repr__(self ):
        return self.title
    
# class fav_books(db.Model):
#     user = db.Column("username",db.String(50),db.ForeignKey("user.username"), primary_key =True)
#     book = db.Column("id_book",db.Integer, db.ForeignKey("book.id"), primary_key =True)

class User(db.Model,UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    favorites = db.relationship("Book", secondary=fav_books,back_populates="favorites_book")

    def __repr__(self):
        return self.username
    
    def get_id(self):
        return self.username

# Get

def get_sample(limit = 10):
    return Book.query.limit(limit).all()

def get_sample_authors(lim = 10):
    return Author.query.limit(lim).all()

def get_book_by_id(id:int):
    return Book.query.get_or_404(id)

def get_author_by_id(id:int):
    return Author.query.get_or_404(id)

def get_books_by_author(id:int):
    return Author.query.get_or_404(id).books.all()

def get_user_by_username(username:str):
    return User.query.get_or_404(username)

def get_fav_books_by_username(username:str):
    return User.query.get_or_404(username).favorites

def get_book_by_title(book_title):
    # res = Book.query.filter(Book.title.startswith(book_title)).all()
    # if res == []:
    #     res = Book.query.filter(Book.title.contains(book_title))
    # return res
    res = Book.query.filter(Book.title.startswith(book_title)).all()
    res2 = Book.query.filter(Book.title.contains(book_title)).all()
    for book in res2:
        if book not in res:
            res.append(book)
    return res

def get_athor_by_name(athor_name):
    res = Author.query.filter(Author.name.startswith(athor_name)).all()
    res2 = Author.query.filter(Author.name.contains(athor_name)).all()
    for author in res2:
        if author not in res:
            res.append(author)
    return res

# Favorites

def add_favorites(user,id_book:int):
    book = get_book_by_id(id_book)
    if book not in user.favorites:
        user.favorites.append(book)
        db.session.commit()

def recommendations(user):
    """ Prend 5 livres au hasard parmis
        Les livres des auteurs des livres favoris

    Args:
        user (): Utilisateur
    """
    fav_books = user.favorites
    authors = {book.author for book in fav_books}
    recommends = []
    for author in authors:
        author_books = get_books_by_author(author.id)
        for book in author_books:
            if book not in fav_books:
                recommends.append(book)
    if len(recommends)>5:
        recommends = random.sample(recommends,5)
    return recommends

def supp_favorites(user,id_book:int):
    book = get_book_by_id(id_book)
    if book in user.favorites:
        user.favorites.remove(book)
        db.session.commit()

# User

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

# Search Bar